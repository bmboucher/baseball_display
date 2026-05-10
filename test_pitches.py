import baseball

_, g = baseball.get_game_from_url("2026-05-04", "NYM", "COL", 1)

pitches: list[baseball.Pitch] = []

for inningIdx, inning in enumerate(g.inning_list, start=1):
    for half in ["top", "bottom"]:
        print(f"{half} half of inning {inningIdx}")
        runs = 0
        appearance_list: list[baseball.PlateAppearance] = getattr(
            inning, f"{half}_half_appearance_list"
        )
        stats = getattr(inning, f"{half}_half_inning_stats")
        expected_runs = stats.R if stats else 0

        for appearance in appearance_list:
            for event in appearance.event_list:
                if isinstance(event, baseball.RunnerAdvance):
                    print(f"{event.start_base} -> {event.end_base}")
                    print(event.run_description)
                    print(event.run_earned)
                    print(event.is_rbi)
            print(appearance.hit_location)
