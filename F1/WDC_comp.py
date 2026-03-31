import fastf1
from fastf1.ergast import Ergast

SEASON = 2026
ROUND = 3

# Get current driver standings
def get_driver_standings():
    ergast = Ergast()
    standings = ergast.get_driver_standings(season=SEASON, round=ROUND)
    return standings.content[0]

# Calculate the max amount of points drivers can get
def calculate_max_points():
    POINTS_SPRINT = 8 + 25 # Max points from sprint weekend
    POINTS_NORMAL = 25 # Max points from normal weekend

    events = fastf1.get_event_schedule(SEASON, backend = 'ergast')
    events = events[events['RoundNumber'] > ROUND]

    sprint_events = len(events.loc[events["EventFormat"] == "sprint_shootout"])
    normal_events = len(events.loc[events["EventFormat"] == "conventional"]) # Conventional is "normal" aka. no sprint

    sprint_points = sprint_events * POINTS_SPRINT
    normal_points = normal_events * POINTS_NORMAL

    return sprint_points + normal_points

# Check who is still able to win the WDC
def calculate_who_can_win(driver_standings, max_points):
    LEADER_POINTS = int(driver_standings.loc[0]['points'])

    for i, _ in enumerate(driver_standings.iterrows()):
        driver = driver_standings.loc[i]
        driver_max_points = int(driver['points']) + max_points
        can_win = 'No' if driver_max_points < LEADER_POINTS else 'Yes'

        print(f"{driver['position']}: {driver['givenName'] + ' ' + driver['familyName']}, "
              f"Current points: {driver['points']}, "
              f"Theoretical max points: {driver_max_points}, "
              f"Can win: {can_win}")
        

driver_standings = get_driver_standings()

points = calculate_max_points()

print("\n")
print('-------------------------------')

print(f"Points left in the season: {points}")

print('-------------------------------')
print("\n")

calculate_who_can_win(driver_standings, points)