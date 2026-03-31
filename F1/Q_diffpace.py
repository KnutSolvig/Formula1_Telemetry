import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta

import fastf1
import fastf1.plotting
from fastf1.core import Laps

# Enable Matlotlib's support for timedelta objects and set the color scheme to 'None' for a more neutral palette
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='None')

# Get session info and load data - update the year, round and session type as needed
session = fastf1.get_session(2020, 6, 'Q')
session.load()

drivers = pd.unique(session.laps['Driver'])
print(drivers)

# Get the fastest lap for each driver and sort them by lap time
list_fastet_laps = list()
for drv in drivers:
    drvs_fastet_lap = session.laps.pick_drivers(drv).pick_fastest()
    list_fastet_laps.append(drvs_fastet_lap)
fastest_laps = Laps(list_fastet_laps) \
    .sort_values(by='LapTime') \
    .reset_index(drop=True)

# Calculate the lap time delta to the pole position lap
pole_lap = fastest_laps.pick_fastest()
fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

print(fastest_laps [['Driver', 'LapTime', 'LapTimeDelta']])

team_colors = list()
for index, lap in fastest_laps.iterrows():
    color = fastf1.plotting.get_team_color(lap['Team'], session = session)
    team_colors.append(color)

fig, ax = plt.subplots()
ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'], 
        color=team_colors, edgecolor='grey')
ax.set_yticks(fastest_laps.index)
ax.set_yticklabels(fastest_laps['Driver'])

ax.invert_yaxis()

ax.set_axisbelow(True)
ax.xaxis.grid(True, which = 'major', linestyle = '--', color = 'black', zorder = 1000)

lap_time_string = strftimedelta(pole_lap['LapTime'], '%M:%S.%ms')

plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
             f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

plt.show()