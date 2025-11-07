import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🌬️ Bio-Inspired Wind Turbine Simulation")
st.write("""
Compare the efficiency of a **normal wind turbine** vs a **bio-inspired (humpback whale fin)** design.
Adjust the parameters below and observe the results.
""")

# Adjustable parameters
wind_speed = st.slider("Wind Speed (m/s)", 2.0, 20.0, 10.0)
blade_angle = st.slider("Blade Angle of Attack (°)", 0.0, 20.0, 10.0)
tubercle_depth = st.slider("Tubercle Depth (Bio Design Only)", 0.0, 1.0, 0.5)
air_density = 1.225  # kg/m^3
blade_area = 10  # m^2


# Simple lift and drag model
def lift_drag_coeff(angle, bio=False, tub_depth=0.0):
    base_cl = 0.1 * angle
    base_cd = 0.01 * (angle ** 2)

    if bio:
        # Bio-inspired improvement: smoother stall, better lift/drag
        cl = base_cl * (1 + 0.2 * tub_depth)
        cd = base_cd * (1 - 0.3 * tub_depth)
    else:
        cl, cd = base_cl, base_cd
    return cl, cd


angles = np.linspace(0, 20, 100)
normal_cl, normal_cd = zip(*[lift_drag_coeff(a, False) for a in angles])
bio_cl, bio_cd = zip(*[lift_drag_coeff(a, True, tubercle_depth) for a in angles])


# Power estimation (simplified)
def power(cl, cd, wind):
    efficiency = cl / (cd + 1e-6)
    return 0.5 * air_density * blade_area * (wind ** 3) * (efficiency / 100)


normal_power = power(*lift_drag_coeff(blade_angle, False), wind_speed)
bio_power = power(*lift_drag_coeff(blade_angle, True, tubercle_depth), wind_speed)

# Plot
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(angles, normal_cl, label="Normal Lift")
ax[0].plot(angles, bio_cl, label="Bio-Inspired Lift", linestyle="--")
ax[0].set_xlabel("Angle of Attack (°)")
ax[0].set_ylabel("Lift Coefficient")
ax[0].legend()

ax[1].bar(["Normal", "Bio-Inspired"], [normal_power, bio_power], color=["skyblue", "lightgreen"])
ax[1].set_ylabel("Estimated Power (W)")
ax[1].set_title("Power Output Comparison")

st.pyplot(fig)

st.subheader("Results")
st.write(f"**Normal Turbine Power:** {normal_power:.2f} W")
st.write(f"**Bio-Inspired Turbine Power:** {bio_power:.2f} W")
st.write(f"💡 Efficiency Gain: {(bio_power / normal_power - 1) * 100:.1f}%")