import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt

fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

# Get session info and load data - update the year, round and session type as needed
session = fastf1.get_session(2026, 2, 'R') 
session.load(telemetry=False, weather = False)

# Defines size of the plot
fig, ax = plt.subplots(figsize =(8.0, 4.9))

# Loop through all drivers in the session and plot their position over laps (Instead of driver number, 
# we use the driver abbreviation for better readability)
for drv in session.drivers:
    drv_laps = session.laps.pick_drivers(drv)

    abb = drv_laps['Driver'].iloc[0]
    style = fastf1.plotting.get_driver_style(identifier=abb,
                                             style = ['color', 'linestyle'],
                                             session=session)
    ax.plot(drv_laps['LapNumber'], drv_laps['Position'],
            label=abb, **style)
    ax.set_ylim([20.5, 0.5])
    # ax.set_yticks([1, 5, 10, 15, 20, 22]) # Different from example on F1Fast because of the number of drivers in the 2026 season
    ax.set_yticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]) # Every position instead of intervals of 5 for better readability
    ax.set_ylabel('Position')
    ax.legend(bbox_to_anchor=(1.0, 1.02))
    plt.tight_layout()


plt.show()