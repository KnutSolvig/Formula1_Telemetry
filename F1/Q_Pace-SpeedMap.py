import fastf1
import fastf1.plotting
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from fastf1.core import Laps
import pandas as pd
from timple.timedelta import strftimedelta

## Uncomment if you want to change the year manually every time the code is run
# year = int(input('Year: '))

year = 2026
round = str(input('Race Circut: '))

session = fastf1.get_session(year, round, 'Q') # Needs to be Q = QUALIFYING
driver = input("Driver abbreviation (e.g. 'VER' for Max Verstappen): ")


session.load()

lap = session.laps.pick_drivers(driver).pick_fastest()
tel = lap.get_telemetry()

x = tel['X'].to_numpy()
y = tel['Y'].to_numpy()
speed = tel['Speed'].to_numpy()

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('equal')
ax.axis('off')

# GET FULL DRIVER NAME
driver_full_name = session.get_driver(driver)['FullName']

norm = plt.Normalize(speed.min(), speed.max())
lc = LineCollection(segments, cmap='plasma', norm=norm)
lc.set_array(speed[:-1])
lc.set_linewidth(4)

ax.add_collection(lc)
colorlegend = plt.colorbar(lc, ax=ax, pad=0.02)
colorlegend.set_label('Speed (km/h)')

plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying \n Heatmap of {driver_full_name}'s fastest lap")

ax.autoscale()
ax.margins(0.05)




##### DIFFERENCE IN FASTEST LAP #####

# Enable Matlotlib's support for timedelta objects and set the color scheme to 'None' for a more neutral palette
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='None')


session = fastf1.get_session(year, round, 'Q') # Needs to be Q = QUALIFYING!
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

lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
             f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

plt.show()

# x = tel['X']
# y = tel['Y']

# plt.figure(figsize=(8, 6))
# plt.plot(x, y)
# plt.axis('equal')
# plt.show()
