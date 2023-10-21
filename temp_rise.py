import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

# Create the first plot
# Create a single subplot for both plots
fig, axs = plt.subplots(1, 1, figsize=(6.4, 3.85))

# Constants
total_resistance = 2.735  # Ohms
specific_heat_capacity_water = 4.186  # J/(g·°C)
currents_continuous = np.linspace(0, 5, 100)
# Adjust the range and number of points as needed
flow_rates_liters_per_min = np.linspace(0.2, 4, 200)

# Define a color map for changing colors with current
color_map = plt.get_cmap('YlOrRd')

# Initialize lists to store temperature rise data
temperature_rise_data = []

for i, current in enumerate(currents_continuous):
    dissipated_powers = current ** 2 * total_resistance
    temperature_rise = dissipated_powers / \
        (flow_rates_liters_per_min / 60 * 1000 * specific_heat_capacity_water)

    # Append temperature rise data to the list
    temperature_rise_data.append(temperature_rise)

    # Get a color from the color map based on the current value
    color = color_map(current / 6.0)

    # Create the temperature rise plot
    axs.plot(flow_rates_liters_per_min, temperature_rise, color=color)

# Create a color bar indicating the current range from 1A to 5A
sm = plt.cm.ScalarMappable(cmap=color_map, norm=plt.Normalize(vmin=1, vmax=5))
sm.set_array([])  # You need to set an empty array for the color bar

# Use make_axes_locatable to create a new axis for the colorbar
divider = make_axes_locatable(axs)
cax = divider.append_axes("right", size="3%", pad=0.15)

# Add the colorbar to the new axis
cbar = plt.colorbar(sm, cax=cax)
cbar.set_label('Current (A)')

# Calculate temperature rise for current = 3A
current_3amps = 3
temperature_rise_3amps = (current_3amps ** 2 * total_resistance) / \
    (flow_rates_liters_per_min / 60 * 1000 * specific_heat_capacity_water)

# Plot temperature rise for current = 3A in black with a dashed line
axs.plot(flow_rates_liters_per_min, temperature_rise_3amps,
         color='black', linestyle='--', linewidth=1, label='Current = 3 A')

# MEASUREMENTS -------------------------------------------------------------------------
# tempertaure rise measurement in the coil running at I = 3A, and I change the flow rate from 0.5 to 4 lit/min
# I used ThermoTeck T257P chiller and used PC cooling solution inside the chiller
# Thermometer that I used was OMEGA HH12A

# Measured flow rates in Lit/min
flow_rate = [0.4, 1.2, 2.0, 2.8, 3.6]

# Measured temperature rise data in °C
T_in_coil_20 = 20
T_out_coil_20 = [20.7, 20.4, 20.3, 20.2, 20.1]

# Calculate temperature rise from measurements
Temp_rise_20 = [x - T_in_coil_20 for x in T_out_coil_20]

# Error bars for temperature rise measurements
xerr = 0.1  # Error in flow rate measurement
# Precision of 0.1°C is valid for flow rate >= 0.6 LPM according to the ThermoTeck T257P
yerr = [0.2, 0.1, 0.1, 0.1, 0.08]

# Scatter plot of temperature rise measurements with error bars
# Adjust 's' to the desired point size
axs.scatter(flow_rate, Temp_rise_20, color="black",
            label='Measurement at $T_{in}$=20°C', zorder=2)
axs.errorbar(flow_rate, Temp_rise_20, xerr=xerr, yerr=yerr,
             fmt='none', ecolor='black', capsize=3)

# Set labels and limits for the temperature rise plot
axs.set_xlabel('Water Flow Rate (Lit/min)')
axs.set_ylabel('Temperature Rise In BioCoil (°C)')
axs.set_xlim(0.2, 4)
axs.set_ylim(0, 1.5)

# Show the legend for the temperature rise plot
axs.legend()

# Adjust the layout
plt.tight_layout()
output_image_path = 'TempRise_BioCoil.png'
plt.savefig(output_image_path, bbox_inches='tight', dpi=200)
plt.show()
