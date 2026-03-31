import matplotlib.pyplot as plt

import fastf1.plotting

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')

# Change year and round as needed
year = 2026
round = 3 # Use number or name 'Spanish Grand Prix'
driver1 = 'ANT' # Driver no. 1 to compare, use abbreviated name
driver2 = 'BOT' # Driver no. 2 to compare, use abbreviated name

session = fastf1.get_session(year, round, 'Q') # Needs to be Q = QUALIFYING
session.load()



drv1_lap = session.laps.pick_drivers(driver1).pick_fastest()
drv2_lap = session.laps.pick_drivers(driver2).pick_fastest()

# Retrieve the telemetry data and add distanse for readability
drv1_tel = drv1_lap.get_car_data().add_distance()
drv2_tel = drv2_lap.get_car_data().add_distance()

drv1_color = fastf1.plotting.get_team_color(drv1_lap['Team'], session=session)
drv2_color = fastf1.plotting.get_team_color(drv2_lap['Team'], session=session)

fig, ax = plt.subplots()
ax.plot(drv1_tel['Distance'], drv1_tel['Speed'], color=drv1_color, label=driver1)
ax.plot(drv2_tel['Distance'], drv2_tel['Speed'], color=drv2_color, label=driver2)

ax.set_xlabel('Distance in meters')
ax.set_ylabel('Speed in km/h')

ax.legend()
plt.suptitle(f"Fastest Lap Comparison \n"
             f"{session.event['EventName']} {session.event.year} Qualifying")

plt.show()



