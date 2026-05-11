import baseball_display.display_constants as dc
from baseball_display.components import (
    BattingOrder,
    BlankScreen,
    ClockDisplay,
    CountDisplay,
    Field,
    GameCountdown,
    GamePreview,
    GameSelect,
    MainMenu,
    PAEvents,
    PitchDisplay,
    PlayerSelect,
    PlayerStatsPanel,
    Scoreboard,
    ScreenBuffer,
    SettingsMenu,
)
from baseball_display.state import DisplayMode


class LeftJumbotron(ScreenBuffer):
    def __init__(self) -> None:
        super().__init__(*dc.SCREENS_LEFT_JUMBOTRON_POS)
        self.blank_screen = BlankScreen()
        self.main_menu = MainMenu()
        self.game_select = GameSelect()
        self.pa_events = PAEvents()
        self.pitch_display = PitchDisplay()
        self.count_display = CountDisplay()
        self.clock_display = ClockDisplay()
        self.scoreboard = Scoreboard()
        self.game_countdown = GameCountdown()
        self.settings_menu = SettingsMenu()
        self.player_select = PlayerSelect()

    def get_active_components(self, mode: DisplayMode):
        if mode == DisplayMode.PLAYERS:
            yield self.player_select
        elif mode == DisplayMode.SETTINGS:
            yield self.settings_menu
        elif mode == DisplayMode.MAIN_MENU:
            yield self.main_menu
        elif mode == DisplayMode.GAME_SELECT:
            yield self.game_select
        elif mode in (DisplayMode.REPLAY, DisplayMode.LIVE):
            yield self.scoreboard
            yield self.pitch_display
            yield self.pa_events
            yield self.count_display
            yield self.clock_display
        elif mode == DisplayMode.PREVIEW:
            yield self.game_countdown
        else:
            yield self.blank_screen


class RightJumbotron(ScreenBuffer):
    def __init__(self) -> None:
        super().__init__(*dc.SCREENS_RIGHT_JUMBOTRON_POS)
        self.blank_screen = BlankScreen()
        self.batting_order = BattingOrder()
        self.game_preview = GamePreview()
        self.player_stats_panel = PlayerStatsPanel()

    def get_active_components(self, mode: DisplayMode):
        if mode == DisplayMode.PLAYERS:
            yield self.player_stats_panel
        elif mode in (DisplayMode.REPLAY, DisplayMode.LIVE):
            yield self.batting_order
        elif mode in (DisplayMode.GAME_SELECT, DisplayMode.PREVIEW):
            yield self.game_preview
        else:
            yield self.blank_screen


class Diamond(ScreenBuffer):
    def __init__(self) -> None:
        super().__init__(*dc.SCREENS_DIAMOND_POS)
        self.field = Field()

    def get_active_components(self, mode: DisplayMode):
        # Field always draws the diagram; it suppresses player overlays
        # itself when mode is not LIVE/REPLAY.
        yield self.field


SCREEN_NAMES: tuple[str, ...] = ("left", "right", "diamond")


def build_screen(name: str) -> ScreenBuffer:
    if name == "left":
        screen: ScreenBuffer = LeftJumbotron()
    elif name == "right":
        screen = RightJumbotron()
    elif name == "diamond":
        screen = Diamond()
    else:
        raise ValueError(f"unknown screen name: {name!r}")
    # In multi-process mode each child owns a 480x320 display, so the panel
    # offset used to position it inside the single-process 1440x320 layout
    # must be zeroed out — otherwise the right/diamond blits land off-screen.
    screen._offset = (0, 0)
    return screen
