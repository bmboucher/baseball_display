from math import sqrt

import pygame

import baseball_display.display_constants as dc
from baseball_display.components.base import Component, make_font
from baseball_display.state import (
    DisplayMode,
    RunnerAnimationMove,
    get_game_display_data,
    get_state,
)


def _base_waypoints(
    start_base: str, end_base: str
) -> list[tuple[int, int]]:
    """Return base-center coordinates the runner passes through, following baselines."""
    ring = dc.FIELD_BASE_ORDER_RING
    if start_base not in ring or end_base not in ring:
        # Fallback: straight line (should not happen with valid data)
        pts: list[tuple[int, int]] = []
        if start_base in dc.FIELD_BASE_CENTERS:
            pts.append(dc.FIELD_BASE_CENTERS[start_base])
        if end_base in dc.FIELD_BASE_CENTERS:
            pts.append(dc.FIELD_BASE_CENTERS[end_base])
        return pts or [dc.FIELD_BASE_CENTERS.get(start_base, (0, 0))]
    si = ring.index(start_base)
    ei = ring.index(end_base)
    waypoints: list[tuple[int, int]] = []
    i = si
    while True:
        waypoints.append(dc.FIELD_BASE_CENTERS[ring[i]])
        if i == ei:
            break
        i = (i + 1) % len(ring)
    return waypoints


# one-time draw of the background; cached and blitted by Field component each frame
def _draw_field(surface: pygame.Surface):
    surface.fill(dc.FIELD_COLOR_BG)
    pygame.draw.circle(
        surface,
        dc.FIELD_COLOR_FIELD,
        (dc.FIELD_MOUND_LEFT, dc.FIELD_MOUND_TOP),
        int(dc.FIELD_OUTFIELD_RADIUS),
        width=dc.FIELD_ZERO_WIDTH,
    )
    pygame.draw.rect(
        surface,
        dc.FIELD_COLOR_BG,
        pygame.Rect(
            int(dc.FIELD_OFFSET),
            0,
            dc.FIELD_SCREEN_W - int(dc.FIELD_OFFSET),
            dc.FIELD_SCREEN_H,
        ),
        width=dc.FIELD_ZERO_WIDTH,
    )
    pygame.draw.rect(
        surface,
        dc.FIELD_COLOR_INFIELD,
        pygame.Rect(
            int(dc.FIELD_OFFSET - dc.FIELD_DIAMOND_SIZE),
            int(dc.FIELD_SCREEN_H - dc.FIELD_DIAMOND_SIZE),
            int(dc.FIELD_DIAMOND_SIZE),
            int(dc.FIELD_DIAMOND_SIZE),
        ),
        width=dc.FIELD_ZERO_WIDTH,
    )
    pygame.draw.rect(
        surface,
        dc.FIELD_BASE_OUTLINE_COLOR,
        pygame.Rect(
            int(dc.FIELD_OFFSET - dc.FIELD_DIAMOND_SIZE + dc.FIELD_BASE_SIZE / 2 - 1),
            int(
                dc.FIELD_SCREEN_H
                - dc.FIELD_DIAMOND_SIZE
                + dc.FIELD_BASE_SIZE / 2
                - 1
            ),
            int(dc.FIELD_DIAMOND_SIZE - dc.FIELD_BASE_SIZE + 2),
            int(dc.FIELD_DIAMOND_SIZE - dc.FIELD_BASE_SIZE + 2),
        ),
        width=dc.FIELD_BASE_OUTLINE_WIDTH,
    )
    for x in [
        int(dc.FIELD_OFFSET - dc.FIELD_DIAMOND_SIZE + 1),
        int(dc.FIELD_OFFSET - 1 - dc.FIELD_BASE_SIZE),
    ]:
        for y in [
            int(dc.FIELD_SCREEN_H - dc.FIELD_DIAMOND_SIZE + 1),
            int(dc.FIELD_SCREEN_H - 1 - dc.FIELD_BASE_SIZE),
        ]:
            pygame.draw.rect(
                surface,
                dc.FIELD_BASE_OUTLINE_COLOR,
                pygame.Rect(x, y, dc.FIELD_BASE_SIZE, dc.FIELD_BASE_SIZE),
                width=dc.FIELD_ZERO_WIDTH,
            )


def _draw_field_mask(surface: pygame.Surface) -> None:
    """Draw an alpha mask of the playable field region for clipping overlays."""
    surface.fill(dc.FIELD_MASK_CLEAR_COLOR)
    pygame.draw.circle(
        surface,
        dc.FIELD_MASK_OPAQUE_COLOR,
        (dc.FIELD_MOUND_LEFT, dc.FIELD_MOUND_TOP),
        int(dc.FIELD_OUTFIELD_RADIUS),
        width=dc.FIELD_ZERO_WIDTH,
    )
    pygame.draw.rect(
        surface,
        dc.FIELD_MASK_OPAQUE_COLOR,
        pygame.Rect(
            int(dc.FIELD_OFFSET - dc.FIELD_DIAMOND_SIZE),
            int(dc.FIELD_SCREEN_H - dc.FIELD_DIAMOND_SIZE),
            int(dc.FIELD_DIAMOND_SIZE),
            int(dc.FIELD_DIAMOND_SIZE),
        ),
        width=dc.FIELD_ZERO_WIDTH,
    )
    # Keep overlays off the right-side non-field panel.
    pygame.draw.rect(
        surface,
        dc.FIELD_MASK_CLEAR_COLOR,
        pygame.Rect(
            int(dc.FIELD_OFFSET),
            0,
            dc.FIELD_SCREEN_W - int(dc.FIELD_OFFSET),
            dc.FIELD_SCREEN_H,
        ),
        width=dc.FIELD_ZERO_WIDTH,
    )


def _draw_rotated_badge(
    surface: pygame.Surface,
    number: str,
    center: tuple[int, int],
    bg_color: tuple[int, int, int],
    font_size: int,
    pad_x: int,
) -> None:
    if not number:
        return
    font = make_font(font_size, bold=True)
    text = font.render(number, True, dc.FIELD_COLOR_NUMBER_BADGE_FG)
    badge_w = text.get_width() + pad_x * 2
    badge_h = font.get_height()

    badge = pygame.Surface((badge_w, badge_h), pygame.SRCALPHA)
    pygame.draw.rect(
        badge,
        bg_color,
        pygame.Rect(0, 0, badge_w, badge_h),
        border_radius=dc.FIELD_BADGE_BORDER_RADIUS,
    )
    badge.blit(text, (pad_x, (badge_h - text.get_height()) // 2))

    rotated = pygame.transform.rotate(badge, dc.FIELD_BADGE_ROTATION_DEGREES)
    rect = rotated.get_rect(center=center)
    surface.blit(rotated, rect)


def _draw_pitcher_mound_badge(surface: pygame.Surface) -> None:
    dd = get_game_display_data()
    pitcher_info = dd.pitcher_info
    if pitcher_info is None or not pitcher_info.number:
        return

    badge_bg = (
        dc.FIELD_COLOR_NUMBER_BADGE_HOME_BG
        if dd.batting_is_away
        else dc.FIELD_COLOR_NUMBER_BADGE_AWAY_BG
    )
    _draw_rotated_badge(
        surface=surface,
        number=pitcher_info.number.zfill(2),
        center=(dc.FIELD_MOUND_LEFT, dc.FIELD_MOUND_TOP),
        bg_color=badge_bg,
        font_size=dc.FIELD_MOUND_BADGE_FONT_SIZE,
        pad_x=dc.FIELD_MOUND_BADGE_PAD_X,
    )


def _draw_home_plate_catcher_badge(surface: pygame.Surface) -> None:
    dd = get_game_display_data()
    catcher_id = dd.home_catcher_id if dd.batting_is_away else dd.away_catcher_id
    if catcher_id is None:
        return
    number = dd.defender_numbers_by_id.get(catcher_id)
    if not number:
        return
    badge_bg = (
        dc.FIELD_COLOR_NUMBER_BADGE_HOME_BG
        if dd.batting_is_away
        else dc.FIELD_COLOR_NUMBER_BADGE_AWAY_BG
    )
    center = (
        dc.FIELD_HOME_PLATE_CENTER[0] - dc.FIELD_DEFENDER_SHIFT_UP_LEFT_PX,
        dc.FIELD_HOME_PLATE_CENTER[1] - dc.FIELD_DEFENDER_SHIFT_UP_LEFT_PX,
    )
    _draw_rotated_badge(
        surface=surface,
        number=number.zfill(2),
        center=center,
        bg_color=badge_bg,
        font_size=dc.FIELD_DEFENDER_BADGE_FONT_SIZE,
        pad_x=dc.FIELD_DEFENDER_BADGE_PAD_X,
    )


def _draw_base_runner_badges(
    surface: pygame.Surface,
    exclude_player_ids: set[int] | None = None,
) -> None:
    dd = get_game_display_data()
    if not dd.runner_ids_by_base:
        return

    excluded = exclude_player_ids or set()

    badge_bg = (
        dc.FIELD_COLOR_NUMBER_BADGE_AWAY_BG
        if dd.batting_is_away
        else dc.FIELD_COLOR_NUMBER_BADGE_HOME_BG
    )
    for base_key in ("home", "1b", "2b", "3b"):
        player_id = dd.runner_ids_by_base.get(base_key)
        if player_id is None or player_id in excluded:
            continue
        number = dd.runner_numbers_by_id.get(player_id) or dd.runner_numbers_by_base.get(
            base_key
        )
        if not number:
            continue
        _draw_rotated_badge(
            surface=surface,
            number=number.zfill(2),
            center=dc.FIELD_BASE_CENTERS[base_key],
            bg_color=badge_bg,
            font_size=dc.FIELD_RUNNER_BADGE_FONT_SIZE,
            pad_x=dc.FIELD_RUNNER_BADGE_PAD_X,
        )


def _draw_highlighted_segments(
    surface: pygame.Surface,
    segments: list[tuple[str, str]],
) -> None:
    for start_base, end_base in segments:
        start = dc.FIELD_BASE_CENTERS.get(start_base)
        end = dc.FIELD_BASE_CENTERS.get(end_base)
        if start is None or end is None:
            continue

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        seg_len = sqrt(dx * dx + dy * dy)
        if seg_len <= 0:
            continue
        ux = dx / seg_len
        uy = dy / seg_len
        inset = dc.FIELD_BASE_SIZE / 2.0
        line_start = (int(start[0] + ux * inset), int(start[1] + uy * inset))
        line_end = (int(end[0] - ux * inset), int(end[1] - uy * inset))

        pygame.draw.line(
            surface,
            dc.FIELD_ANIM_SEGMENT_COLOR,
            line_start,
            line_end,
            dc.FIELD_ANIM_SEGMENT_WIDTH,
        )


def _draw_dashed_line(
    surface: pygame.Surface,
    color: tuple[int, int, int],
    start: tuple[int, int],
    end: tuple[int, int],
    width: int,
    dash_length: int,
    gap_length: int,
) -> None:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = sqrt(dx * dx + dy * dy)
    if length <= 0:
        return

    ux = dx / length
    uy = dy / length
    dist = 0.0
    while dist < length:
        seg_end = min(dist + dash_length, length)
        s = (int(start[0] + ux * dist), int(start[1] + uy * dist))
        e = (int(start[0] + ux * seg_end), int(start[1] + uy * seg_end))
        pygame.draw.line(surface, color, s, e, width)
        dist += dash_length + gap_length


class Field(Component):
    def __init__(self):
        super().__init__()
        self._base = pygame.Surface((dc.FIELD_SCREEN_W, dc.FIELD_SCREEN_H))
        _draw_field(self._base)
        self._field_mask = pygame.Surface(
            (dc.FIELD_SCREEN_W, dc.FIELD_SCREEN_H), pygame.SRCALPHA
        )
        _draw_field_mask(self._field_mask)
        self._overlay = pygame.Surface(
            (dc.FIELD_SCREEN_W, dc.FIELD_SCREEN_H), pygame.SRCALPHA
        )
        self._anim_pa_token: tuple[int, bool, int] | None = None
        self._anim_play_index: int | None = None
        self._anim_move_signature: tuple[
            tuple[int, str, str | None, bool, int], ...
        ] = ()
        self._anim_phase: str = "move"
        self._anim_phase_start_ms: int = pygame.time.get_ticks()
        self._anim_group_move_ms: int = dc.FIELD_ANIM_BASE_MOVE_MS

    def _reset_runner_animation(
        self,
        pa_token: tuple[int, bool, int] | None,
        play_index: int | None,
        group_move_ms: int | None = None,
    ) -> None:
        self._anim_pa_token = pa_token
        self._anim_play_index = play_index
        self._anim_move_signature = ()
        self._anim_phase = "move"
        self._anim_phase_start_ms = pygame.time.get_ticks()
        self._anim_group_move_ms = max(1, group_move_ms or dc.FIELD_ANIM_BASE_MOVE_MS)

    @staticmethod
    def _path_length(path: list[tuple[int, int]]) -> float:
        if len(path) < 2:
            return 0.0
        total = 0.0
        for i in range(len(path) - 1):
            dx = path[i + 1][0] - path[i][0]
            dy = path[i + 1][1] - path[i][1]
            total += sqrt(dx * dx + dy * dy)
        return total

    @staticmethod
    def _one_base_distance() -> float:
        dx = dc.FIELD_FIRST_BASE_CENTER[0] - dc.FIELD_HOME_PLATE_CENTER[0]
        dy = dc.FIELD_FIRST_BASE_CENTER[1] - dc.FIELD_HOME_PLATE_CENTER[1]
        return sqrt(dx * dx + dy * dy)

    def _move_path_for_runner(
        self,
        move: RunnerAnimationMove,
    ) -> list[tuple[int, int]]:
        start = dc.FIELD_BASE_CENTERS.get(move.start_base)
        if start is None:
            return []
        if (
            not move.is_out
            and move.start_base == "home"
            and move.end_base == "home"
        ):
            # Home runs trace the full basepath home->1b->2b->3b->home, then
            # continue past home plate until the badge exits the field mask.
            return [
                dc.FIELD_BASE_CENTERS["home"],
                dc.FIELD_BASE_CENTERS["1b"],
                dc.FIELD_BASE_CENTERS["2b"],
                dc.FIELD_BASE_CENTERS["3b"],
                dc.FIELD_BASE_CENTERS["home"],
                dc.FIELD_HOME_SCORE_EXIT_POINT,
            ]
        if move.is_out:
            if move.end_base is not None:
                waypoints = _base_waypoints(move.start_base, move.end_base)
                if not waypoints:
                    return []
                if len(waypoints) >= 2:
                    prev_pt = waypoints[-2]
                    out_base_pt = waypoints[-1]
                    out_target = (
                        int((prev_pt[0] + out_base_pt[0]) / 2),
                        int((prev_pt[1] + out_base_pt[1]) / 2),
                    )
                    anim_waypoints = list(waypoints)
                    anim_waypoints[-1] = out_target
                    return anim_waypoints
                return waypoints
            next_base = dc.FIELD_NEXT_BASE_FOR_PATH.get(move.start_base)
            if next_base is None:
                return []
            next_center = dc.FIELD_BASE_CENTERS.get(next_base)
            if next_center is None:
                return []
            out_target = (
                int((start[0] + next_center[0]) / 2),
                int((start[1] + next_center[1]) / 2),
            )
            return [start, out_target]
        if move.end_base is None:
            return []
        path = _base_waypoints(move.start_base, move.end_base)
        if move.end_base == "home":
            # Extend the path past home plate so the badge exits the field mask.
            path.append(dc.FIELD_HOME_SCORE_EXIT_POINT)
        return path

    def _move_duration_ms_for_path(self, path: list[tuple[int, int]]) -> int:
        length = self._path_length(path)
        one_base = self._one_base_distance()
        if length <= 0 or one_base <= 0:
            return dc.FIELD_ANIM_BASE_MOVE_MS
        # Constant speed: one-base distance takes FIELD_ANIM_BASE_MOVE_MS.
        duration = int(round((length / one_base) * dc.FIELD_ANIM_BASE_MOVE_MS))
        return max(1, duration)

    def _group_move_duration_ms(self, moves: list[RunnerAnimationMove]) -> int:
        max_ms = dc.FIELD_ANIM_BASE_MOVE_MS
        for move in moves:
            path = self._move_path_for_runner(move)
            if not path:
                continue
            max_ms = max(max_ms, self._move_duration_ms_for_path(path))
        return max_ms

    def _animation_progress(self) -> tuple[int, bool]:
        now = pygame.time.get_ticks()
        elapsed = now - self._anim_phase_start_ms
        if self._anim_phase == "move":
            if elapsed >= self._anim_group_move_ms:
                self._anim_phase = "pause"
                self._anim_phase_start_ms = now
                return self._anim_group_move_ms, True
            return elapsed, False

        if elapsed >= dc.FIELD_ANIM_PAUSE_MS:
            self._anim_phase = "move"
            self._anim_phase_start_ms = now
            return 0, False
        return self._anim_group_move_ms, True

    @staticmethod
    def _interpolate(
        start: tuple[int, int],
        end: tuple[int, int],
        t: float,
    ) -> tuple[int, int]:
        return (
            int(start[0] + (end[0] - start[0]) * t),
            int(start[1] + (end[1] - start[1]) * t),
        )

    @staticmethod
    def _interpolate_waypoints(
        waypoints: list[tuple[int, int]],
        t: float,
    ) -> tuple[int, int]:
        """Interpolate a position along a multi-segment path at normalized t in [0, 1]."""
        if len(waypoints) == 1:
            return waypoints[0]
        n_segs = len(waypoints) - 1
        seg_t = 1.0 / n_segs
        seg_idx = min(int(t / seg_t), n_segs - 1)
        local_t = (t - seg_idx * seg_t) / seg_t
        s = waypoints[seg_idx]
        e = waypoints[seg_idx + 1]
        return (
            int(s[0] + (e[0] - s[0]) * local_t),
            int(s[1] + (e[1] - s[1]) * local_t),
        )

    @staticmethod
    def _draw_out_marker(
        surface: pygame.Surface,
        center: tuple[int, int],
    ) -> None:
        h = int(dc.FIELD_OUT_MARK_HALF_LEN)
        x, y = center
        pygame.draw.line(
            surface,
            dc.FIELD_OUT_MARK_COLOR,
            (x - h, y - h),
            (x + h, y + h),
            dc.FIELD_OUT_MARK_WIDTH,
        )
        pygame.draw.line(
            surface,
            dc.FIELD_OUT_MARK_COLOR,
            (x + h, y - h),
            (x - h, y + h),
            dc.FIELD_OUT_MARK_WIDTH,
        )

    def _draw_runner_badges(self, surface: pygame.Surface) -> None:
        dd = get_game_display_data()
        move_signature = tuple(
            (
                move.player_id,
                move.start_base,
                move.end_base,
                move.is_out,
                move.play_index,
            )
            for move in dd.runner_animation_moves
        )
        if (
            dd.runner_animation_pa_token != self._anim_pa_token
            or dd.runner_animation_max_play_index != self._anim_play_index
            or move_signature != self._anim_move_signature
        ):
            group_move_ms = self._group_move_duration_ms(dd.runner_animation_moves)
            self._reset_runner_animation(
                dd.runner_animation_pa_token,
                dd.runner_animation_max_play_index,
                group_move_ms,
            )
            self._anim_move_signature = move_signature

        moves = dd.runner_animation_moves
        if not moves:
            _draw_base_runner_badges(surface)
            return

        elapsed_move_ms, in_pause = self._animation_progress()
        moving_ids = {move.player_id for move in moves}
        _draw_base_runner_badges(surface, exclude_player_ids=moving_ids)

        badge_bg = (
            dc.FIELD_COLOR_NUMBER_BADGE_AWAY_BG
            if dd.batting_is_away
            else dc.FIELD_COLOR_NUMBER_BADGE_HOME_BG
        )
        for move in moves:
            number = dd.runner_numbers_by_id.get(move.player_id)
            if not number:
                continue
            start = dc.FIELD_BASE_CENTERS.get(move.start_base)
            if start is None:
                continue
            path = self._move_path_for_runner(move)
            if not path:
                continue
            move_duration_ms = self._move_duration_ms_for_path(path)
            progress = 1.0 if in_pause else min(elapsed_move_ms / move_duration_ms, 1.0)

            if move.is_out:
                out_target = path[-1]
                if in_pause or progress >= 1.0:
                    self._draw_out_marker(surface, out_target)
                    continue
                center = self._interpolate_waypoints(path, progress)
            elif move.end_base is None:
                continue
            else:
                center = path[-1] if in_pause else self._interpolate_waypoints(path, progress)

            _draw_rotated_badge(
                surface=surface,
                number=number.zfill(2),
                center=center,
                bg_color=badge_bg,
                font_size=dc.FIELD_RUNNER_BADGE_FONT_SIZE,
                pad_x=dc.FIELD_RUNNER_BADGE_PAD_X,
            )

    @staticmethod
    def _offset_infielder_badge(
        slot: str,
        center: tuple[int, int],
    ) -> tuple[int, int]:
        # Only 1B/3B need offset because those fielders stand at the bags.
        if slot in {"1b", "3b"}:
            return (
                center[0] - dc.FIELD_DEFENDER_SHIFT_UP_LEFT_PX,
                center[1] - dc.FIELD_DEFENDER_SHIFT_UP_LEFT_PX,
            )
        return center

    def _draw_infield_defender_badges(self, surface: pygame.Surface) -> None:
        dd = get_game_display_data()
        defense_slots = dd.home_infield_slots if dd.batting_is_away else dd.away_infield_slots
        if not defense_slots:
            return

        badge_bg = (
            dc.FIELD_COLOR_NUMBER_BADGE_HOME_BG
            if dd.batting_is_away
            else dc.FIELD_COLOR_NUMBER_BADGE_AWAY_BG
        )
        for slot in ("1b", "2b", "3b", "ss"):
            player_id = defense_slots.get(slot)
            if player_id is None:
                continue
            number = dd.defender_numbers_by_id.get(player_id)
            if not number:
                continue
            anchor = dc.FIELD_INFIELD_SLOT_ANCHORS.get(slot)
            if anchor is None:
                continue
            center = self._offset_infielder_badge(slot, anchor)
            _draw_rotated_badge(
                surface=surface,
                number=number.zfill(2),
                center=center,
                bg_color=badge_bg,
                font_size=dc.FIELD_DEFENDER_BADGE_FONT_SIZE,
                pad_x=dc.FIELD_DEFENDER_BADGE_PAD_X,
            )

    def _draw_outfield_defender_badges(self, surface: pygame.Surface) -> None:
        dd = get_game_display_data()
        defense_slots = dd.home_outfield_slots if dd.batting_is_away else dd.away_outfield_slots
        if not defense_slots:
            return

        badge_bg = (
            dc.FIELD_COLOR_NUMBER_BADGE_HOME_BG
            if dd.batting_is_away
            else dc.FIELD_COLOR_NUMBER_BADGE_AWAY_BG
        )
        for slot in ("lf", "cf", "rf"):
            player_id = defense_slots.get(slot)
            if player_id is None:
                continue
            number = dd.defender_numbers_by_id.get(player_id)
            if not number:
                continue
            anchor = dc.FIELD_OUTFIELD_SLOT_ANCHORS.get(slot)
            if anchor is None:
                continue
            _draw_rotated_badge(
                surface=surface,
                number=number.zfill(2),
                center=anchor,
                bg_color=badge_bg,
                font_size=dc.FIELD_DEFENDER_BADGE_FONT_SIZE,
                pad_x=dc.FIELD_DEFENDER_BADGE_PAD_X,
            )

    def _convert_hit_coordinates(self, raw_x: float, raw_y: float) -> tuple[int, int]:
        """Convert hit data coordinates into a field-space endpoint.

        Input is home-plate-centered and rotated by `-_HIT_ROT_DEG`.
        """
        # Unrotate by +theta to align with field axes.
        raw_x = raw_x - dc.FIELD_HIT_COORDINATE_X_OFFSET
        raw_y = dc.FIELD_HIT_COORDINATE_Y_OFFSET - raw_y

        pos_x = raw_x / dc.FIELD_SQRT_2 - raw_y / dc.FIELD_SQRT_2
        pos_y = raw_x / dc.FIELD_SQRT_2 + raw_y / dc.FIELD_SQRT_2

        return (
            int(dc.FIELD_OFFSET + pos_x * dc.FIELD_TOTAL_SCALE),
            int(dc.FIELD_SCREEN_H - pos_y * dc.FIELD_TOTAL_SCALE),
        )

    def _draw_hit_line(self, surface: pygame.Surface) -> None:
        dd = get_game_display_data()
        hit_pos = dd.last_hit_position
        if hit_pos is None:
            return

        home_x, home_y = dc.FIELD_HOME_PLATE_CENTER
        end_x, end_y = self._convert_hit_coordinates(hit_pos[0], hit_pos[1])

        pygame.draw.line(
            surface,
            dc.FIELD_HIT_LINE_COLOR,
            (home_x, home_y),
            (end_x, end_y),
            dc.FIELD_HIT_LINE_WIDTH,
        )
        pygame.draw.circle(
            surface,
            dc.FIELD_HIT_BALL_COLOR,
            (end_x, end_y),
            dc.FIELD_HIT_BALL_RADIUS,
        )

    def _draw_pickoff_line(self, surface: pygame.Surface) -> None:
        dd = get_game_display_data()
        target_base = dd.pickoff_target_base
        if target_base is None:
            return

        end = dc.FIELD_BASE_CENTERS.get(target_base.lower())
        if end is None:
            return

        _draw_dashed_line(
            surface=surface,
            color=dc.FIELD_HIT_LINE_COLOR,
            start=(dc.FIELD_MOUND_LEFT, dc.FIELD_MOUND_TOP),
            end=end,
            width=dc.FIELD_HIT_LINE_WIDTH,
            dash_length=dc.FIELD_PICKOFF_DASH_LENGTH,
            gap_length=dc.FIELD_PICKOFF_GAP_LENGTH,
        )

    def draw(self, surface: pygame.Surface):
        surface.blit(self._base, (0, 0))
        # Only draw player badges, animations, hit lines, etc. when there's
        # a game in progress. Outside LIVE/REPLAY the field shows just the
        # diagram (no leftover badges from a previous game).
        if get_state().mode not in (DisplayMode.LIVE, DisplayMode.REPLAY):
            return
        self._overlay.fill(dc.FIELD_OVERLAY_CLEAR_COLOR)
        _draw_highlighted_segments(
            self._overlay,
            get_game_display_data().runner_animation_segments,
        )
        self._draw_pickoff_line(self._overlay)
        self._draw_hit_line(self._overlay)
        self._draw_runner_badges(self._overlay)
        self._draw_outfield_defender_badges(self._overlay)
        self._draw_infield_defender_badges(self._overlay)
        _draw_home_plate_catcher_badge(self._overlay)
        _draw_pitcher_mound_badge(self._overlay)
        self._draw_strikeout_k(self._overlay)
        # Clip all dynamic overlays to the field region.
        self._overlay.blit(self._field_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(self._overlay, (0, 0))

    def _draw_strikeout_k(self, surface: pygame.Surface) -> None:
        dd = get_game_display_data()
        if not dd.show_strikeout_k:
            return
        # Flash on/off based on time
        if (pygame.time.get_ticks() // dc.FIELD_STRIKEOUT_K_FLASH_MS) % 2 == 0:
            return
        font = make_font(dc.FIELD_STRIKEOUT_K_FONT_SIZE, bold=True)
        text = font.render(
            dc.FIELD_STRIKEOUT_TEXT,
            True,
            dc.FIELD_STRIKEOUT_K_COLOR,
        )
        # Rotate 45 degrees to align with the diamond
        rotated = pygame.transform.rotate(text, dc.FIELD_STRIKEOUT_ROTATION_DEGREES)
        # Center on the diamond: midpoint between home and 2nd base
        cx = (dc.FIELD_HOME_PLATE_CENTER[0] + dc.FIELD_SECOND_BASE_CENTER[0]) // 2
        cy = (dc.FIELD_HOME_PLATE_CENTER[1] + dc.FIELD_SECOND_BASE_CENTER[1]) // 2
        rect = rotated.get_rect(center=(cx, cy))
        surface.blit(rotated, rect)
