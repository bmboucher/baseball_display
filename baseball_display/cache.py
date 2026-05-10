import hashlib
import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import (
    Any,
    Callable,
    Generic,
    Protocol,
    Type,
    TypeVar,
    TypeVarTuple,
    Unpack,
    cast,
)

from pydantic import BaseModel

logger = logging.getLogger(__name__)

KeyT = TypeVar("KeyT", bound=tuple[Any, ...], infer_variance=True)
ValueT = TypeVar("ValueT", bound=BaseModel, infer_variance=True)
_Ts = TypeVarTuple("_Ts")


def hash_args(args: tuple[Any, ...]) -> str:
    argstr = "-".join(map(str, args))
    return hashlib.sha256(argstr.encode()).hexdigest()


class GetterValidator(Protocol, Generic[KeyT, ValueT]):
    def get(self, key: KeyT) -> ValueT: ...

    def validate(self, key: KeyT, cache_time: float) -> bool: ...


class CacheBase(ABC, GetterValidator[KeyT, ValueT]):
    def __init__(self, inner: GetterValidator[KeyT, ValueT]):
        self.inner = inner

    @abstractmethod
    def get_cache_time(self, key: KeyT) -> float | None:
        raise NotImplementedError

    @abstractmethod
    def get_cached(self, key: KeyT) -> ValueT | None:
        raise NotImplementedError

    @abstractmethod
    def cache(self, key: KeyT, value: ValueT) -> None:
        raise NotImplementedError

    def get(self, key: KeyT) -> ValueT:
        cache_time = self.get_cache_time(key)
        if cache_time is not None:
            if not self.inner.validate(key, cache_time):
                logger.debug(
                    f"Invalidating cache for {key} (cached {time.time()-cache_time:.2f}s ago)"
                )
            else:
                try:
                    cached = self.get_cached(key)
                    if cached is not None:
                        return cached
                    else:
                        logger.error(
                            f"get_cache_time returned a value but get_cached did not for key {key}"
                        )
                except Exception:
                    logger.warning("Failed to read cache for key %s — re-fetching", key)
        cached = self.inner.get(key)
        self.cache(key, cached)
        return cached

    def validate(self, key: KeyT, cache_time: float) -> bool:
        return self.inner.validate(key, cache_time)


class FileCache(CacheBase[KeyT, ValueT]):
    def __init__(
        self,
        inner: GetterValidator[KeyT, ValueT],
        cache_dir: Path,
        mdl: Type[ValueT],
        name: str,
    ):
        super().__init__(inner)
        self.cache_dir = cache_dir
        self.mdl = mdl
        self.name = name

    def get_cache_file_name(self, key: KeyT) -> str:
        return f"{hash_args((self.name,) + tuple(key))}.json"

    def get_cache_path(self, key: KeyT) -> Path:
        return self.cache_dir / self.get_cache_file_name(key)

    def get_cache_time(self, key: KeyT) -> float | None:
        cache_path = self.get_cache_path(key)
        if cache_path.exists():
            return cache_path.stat().st_mtime
        return None

    def get_cached(self, key: KeyT) -> ValueT:
        cache_path = self.get_cache_path(key)
        logger.info(f"Loading from file cache for key {key} at {cache_path}")
        text = cache_path.read_text(encoding="utf-8")
        if not text.strip():
            logger.warning("Empty cache file for key %s — deleting", key)
            cache_path.unlink(missing_ok=True)
            raise ValueError(f"Empty cache file: {cache_path}")
        try:
            return self.mdl.model_validate_json(text)
        except Exception:
            logger.warning("Corrupt cache file for key %s — deleting", key)
            cache_path.unlink(missing_ok=True)
            raise

    def cache(self, key: KeyT, value: ValueT) -> None:
        cache_path = self.get_cache_path(key)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Caching to file for key {key} at {cache_path}")
        cache_path.write_text(value.model_dump_json(indent=2), encoding="utf-8")


class MemoryCache(CacheBase[KeyT, ValueT]):
    def __init__(self, inner: GetterValidator[KeyT, ValueT], maxsize: int = 100):
        super().__init__(inner)
        self._cache: dict[KeyT, tuple[ValueT, float]] = {}
        self._maxsize = maxsize

    def get_cache_time(self, key: KeyT) -> float | None:
        cached = self._cache.get(key)
        if cached is not None:
            return cached[1]
        return None

    def get_cached(self, key: KeyT) -> ValueT | None:
        cached = self._cache.get(key)
        if cached is not None:
            return cached[0]
        return None

    def cache(self, key: KeyT, value: ValueT) -> None:
        self._cache[key] = (value, time.time())
        while len(self._cache) > self._maxsize:
            oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]


class Endpoint(GetterValidator[KeyT, ValueT]):
    def __init__(
        self,
        name: str,
        cache_path: Path,
        mdl: Type[ValueT],
        endpoint: Callable[..., ValueT],
        validator: Callable[..., bool],
    ):
        self.name = name
        self.cache_path = cache_path
        self.mdl = mdl
        self.endpoint = endpoint
        self.validator = validator

    def get(self, key: KeyT) -> ValueT:
        return self.endpoint(*key)

    def validate(self, key: KeyT, cache_time: float) -> bool:
        return self.validator(*key, cache_time)

    def wrap_in_cache(self) -> GetterValidator[KeyT, ValueT]:
        # chain of caches: memory -> file -> http request
        fileCache = FileCache(self, self.cache_path, self.mdl, self.name)
        memoryCache = MemoryCache(fileCache)
        return memoryCache


def make_endpoint(
    name: str,
    cache_path: Path,
    mdl: Type[ValueT],
    endpoint: Callable[[Unpack[_Ts]], ValueT],
    validator: Callable[..., bool],
) -> GetterValidator[tuple[Unpack[_Ts]], ValueT]:
    ep = Endpoint(name, cache_path, mdl, endpoint, validator)  # type: ignore[arg-type]
    return cast(GetterValidator[tuple[Unpack[_Ts]], ValueT], ep.wrap_in_cache())
