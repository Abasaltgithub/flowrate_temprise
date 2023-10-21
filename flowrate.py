import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Parameters for the first plot
D = 0.004  # m (pipe diameter)
L = 2  # m (pipe length)
ε = 0.0000013  # m (absolute roughness of the pipe)
ρ = 998.206  # kg/m^3 (density of water)
A = np.pi * (D/2)**2  # m^2 (cross-sectional area of the pipe)

# Dynamic viscosity of water at 20°C
µ_20C = 0.001002  # Pa·s

# Dynamic viscosity of water at 10°C and 30°C
µ_10C = 0.001308  # Pa·s
µ_30C = 0.000798  # Pa·s

# Range of flow rates to test
Q_range = np.linspace(0, 0.0001, 100)  # m^3/s
Q_range_LPM = Q_range * 60000  # L/min

# Calculate pressure drop for each flow rate at 10°C, 20°C, and 30°C
pressure_drop_10C = []
pressure_drop_20C = []
pressure_drop_30C = []

for Q in Q_range:
    # Include dynamic viscosity at 20°C in Reynolds number calculation
    Re = (4 * Q * ρ) / (np.pi * D * µ_20C)

    if Re == 0:
        f = 0
    else:
        f = 0.25 / ((np.log10((ε/D)/3.7 + (5.74/Re**0.9)))**2)

    ΔP_20C = (f * L * ρ * Q**2) / (2 * D * A**2)
    pressure_drop_20C.append(ΔP_20C / 100000)  # convert Pa to bar

    # Calculate pressure drop at 10°C and 30°C
    Re_10C = (4 * Q * ρ) / (np.pi * D * µ_10C)
    Re_30C = (4 * Q * ρ) / (np.pi * D * µ_30C)

    if Re_10C == 0:
        f_10C = 0
    else:
        f_10C = 0.25 / ((np.log10((ε/D)/3.7 + (5.74/Re_10C**0.9)))**2)

    if Re_30C == 0:
        f_30C = 0
    else:
        f_30C = 0.25 / ((np.log10((ε/D)/3.7 + (5.74/Re_30C**0.9)))**2)

    ΔP_10C = (f_10C * L * ρ * Q**2) / (2 * D * A**2)
    ΔP_30C = (f_30C * L * ρ * Q**2) / (2 * D * A**2)

    pressure_drop_10C.append(ΔP_10C / 100000)  # convert Pa to bar
    pressure_drop_30C.append(ΔP_30C / 100000)  # convert Pa to bar

# Provided data from http://www.pressure-drop.online/
flow_rate_data = [0.2, 1, 1.5, 2, 2.5, 3]  # Lit/min
pressure_drop_data = [0.011, 0.163, 0.329, 0.543, 0.803, 1.108]  # bar

# Define a function for the curve fit (e.g., a polynomial of degree 2)


def curve_func(x, a, b, c):
    return a * x**2 + b * x + c


# Perform the curve fit
fit_params, _ = curve_fit(curve_func, flow_rate_data, pressure_drop_data)

# Create a range of values for the fitted curve
fit_x = np.linspace(0, 3, 100)
fit_y = curve_func(fit_x, *fit_params)

# Create the first plot
fig, axs = plt.subplots(1, 1, figsize=(6, 4))  # Create a single subplot

# Plot the first graph
axs.plot(Q_range_LPM, pressure_drop_20C,
         label='T=20°C (Simulation)', color='darkblue')
axs.fill_between(Q_range_LPM, pressure_drop_10C, pressure_drop_30C,
                 color='lightblue', alpha=0.5, label='T=10-30°C Range')
axs.set_xlabel('Water Flow Rate (Lit/min)')
axs.set_ylabel('Pressure Drop (bar)')
axs.set_xlim(0.1, 2)
axs.set_ylim(0.001, 0.55)
axs.legend()
# plt.title('Pressure Drop vs. Flow Rate')

# Adjust the layout
plt.tight_layout()

# Save the figure
output_image_path = 'FlowRate_PressureDrop.png'
plt.savefig(output_image_path, bbox_inches='tight', dpi=200)

# Show the figure
plt.show()