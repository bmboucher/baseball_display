# mlb_api/ — generated code

This package is **generated** by the schemas → models workflow described
in the project root `CLAUDE.md`. It contains Pydantic v2 models produced
by `datamodel-codegen` from the JSON Schemas in `schemas/`, regenerated
via `scripts/regenerate_models.py`.

**There is no `Client` / `AuthenticatedClient` / `httpx` interface in
this package.** It is models-only. All HTTP traffic to `statsapi.mlb.com`
goes through `baseball_display/statsapi.py` (caching + per-thread
rate-limited wrapper). Use those models, not anything from this folder,
for fetching live data.

To regenerate after the MLB API changes:

```bash
python scripts/build_schemas.py        # refresh JSON schemas from sample responses
python scripts/regenerate_models.py    # regenerate all Pydantic models
# or, target one schema:
python scripts/regenerate_models.py live_game
```

(An older `openapi-python-client` template README previously lived here.
It described an HTTP client API this project does not use and has been
removed to avoid confusion.)
