MIN_TIME_BETWEEN_REQUESTS: int = 10
SCHEDULE_LOOKBACK_DAYS: int = 7
SCHEDULE_LOOKAHEAD_DAYS: int = 2
MLB_SCHEDULE_URL: str = (
    "https://statsapi.mlb.com/api/v1/schedule"
    "?sportId=1&startDate={start}&endDate={end}"
    "&hydrate=dates,games,teams,[home,away],team"
)
MLB_LOGO_URL: str = "https://www.mlbstatic.com/team-logos/{team_id}.svg"
MLB_PLAYER_PHOTO_URL: str = (
    "https://img.mlbstatic.com/mlb-photos/image/upload"
    "/w_213,d_people:generic:headshot:silo:current.png,q_auto:best,f_auto"
    "/v1/people/{mlb_id}/headshot/67/current"
)
REQUEST_TIMEOUT_SECONDS: int = 10

# Maps raw MLB Stats API stat keys to human-readable display labels.
# Used in state.py when computing DisplayData; must not be referenced in display components.
STAT_DISPLAY_NAMES: dict[str, str] = {
    # Hitting
    "airOuts": "Fly Outs",
    "atBats": "At Bats",
    "atBatsPerHomeRun": "AB per Home Run",
    "avg": "Batting Average",
    "babip": "BABIP",
    "baseOnBalls": "Walks",
    "catchersInterference": "Catcher's Interference",
    "caughtStealing": "Caught Stealing",
    "caughtStealingPercentage": "Caught Stealing %",
    "doubles": "Doubles",
    "gamesPlayed": "Games Played",
    "groundIntoDoublePlay": "Grounded Into DP",
    "groundOuts": "Ground Outs",
    "groundOutsToAirouts": "Ground/Fly Ratio",
    "hitByPitch": "Hit By Pitch",
    "hits": "Hits",
    "homeRuns": "Home Runs",
    "intentionalWalks": "Intentional Walks",
    "leftOnBase": "Left On Base",
    "numberOfPitches": "Pitches Seen",
    "obp": "On-Base Percentage",
    "ops": "OPS",
    "plateAppearances": "Plate Appearances",
    "rbi": "Runs Batted In",
    "runs": "Runs Scored",
    "sacBunts": "Sacrifice Bunts",
    "sacFlies": "Sacrifice Flies",
    "slg": "Slugging Percentage",
    "stolenBases": "Stolen Bases",
    "stolenBasePercentage": "Stolen Base %",
    "strikeOuts": "Strikeouts",
    "totalBases": "Total Bases",
    "triples": "Triples",
    # Pitching
    "balks": "Balks",
    "battersFaced": "Batters Faced",
    "blownSaves": "Blown Saves",
    "completeGames": "Complete Games",
    "earnedRuns": "Earned Runs",
    "era": "ERA",
    "gamesPitched": "Games Pitched",
    "gamesFinished": "Games Finished",
    "gamesStarted": "Games Started",
    "hitBatsmen": "Hit Batsmen",
    "hitsPer9Inn": "Hits per 9 Inn",
    "holds": "Holds",
    "homeRunsPer9": "Home Runs per 9",
    "inheritedRunners": "Inherited Runners",
    "inheritedRunnersScored": "Inherited Runners Scored",
    "inningsPitched": "Innings Pitched",
    "losses": "Losses",
    "outs": "Outs Recorded",
    "pickoffs": "Pickoffs",
    "pitchesPerInning": "Pitches per Inning",
    "runsScoredPer9": "Runs per 9 Inn",
    "saveOpportunities": "Save Opportunities",
    "saves": "Saves",
    "shutouts": "Shutouts",
    "strikePercentage": "Strike Percentage",
    "strikes": "Strikes Thrown",
    "strikeoutWalkRatio": "SO/BB Ratio",
    "strikeoutsPer9Inn": "Strikeouts per 9",
    "walksPer9Inn": "Walks per 9 Inn",
    "whip": "WHIP",
    "wildPitches": "Wild Pitches",
    "winPercentage": "Win Percentage",
    "wins": "Wins",
}

# Maps raw MLB Stats API pitch type codes to full display names.
# Used in state.py when computing DisplayData; must not be referenced in display components.
PITCH_TYPE_NAMES: dict[str, str] = {
    "FF": "4S FASTBALL",
    "FA": "FASTBALL",
    "FT": "TWO-SEAM FASTBALL",
    "SI": "SINKER",
    "FC": "CUTTER",
    "SL": "SLIDER",
    "ST": "SWEEPER",
    "SV": "SLURVE",
    "CU": "CURVEBALL",
    "KC": "KNUCKLE CURVE",
    "CS": "SLOW CURVE",
    "CH": "CHANGEUP",
    "FS": "SPLITTER",
    "FO": "FORKBALL",
    "SC": "SCREWBALL",
    "KN": "KNUCKLEBALL",
    "EP": "EEPHUS",
    "IN": "INTENTIONAL BALL",
    "PO": "PITCHOUT",
    "AB": "AUTOMATIC BALL",
    "AS": "AUTOMATIC STRIKE",
    "SB": "SWEEPING CURVE",
}
