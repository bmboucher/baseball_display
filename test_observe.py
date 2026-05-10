import baseball

from baseball_display import state

_, g = baseball.get_game_from_url("2026-05-03", "TOR", "MIN", 1)

dd = state.DisplayData()
rs = state.ReplayState()
rs.inning_index = 4
rs.current_appearance = 1
dd.observe_game(g, rs)
print(dd)

rs.current_appearance = 0
dd.observe_game(g, rs)
print(dd)

rs.inning_index = 7
dd.observe_game(g, rs)
print(dd)

dd.observe_game(g)
print(dd)
