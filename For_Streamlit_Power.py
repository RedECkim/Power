import streamlit as st

# Streamlit에서 사용될 입력 리스트
st.title("Power Estimated Calculation Tools")

# 전체 입력값을 하나의 섹션으로 통합
st.header("Input Parameters")

Ambient_temperature = st.number_input("Ambient Temperature (°C)", value=25.0, step=0.01)
Surface_temperature = st.number_input("Surface Temperature (°C)", value=45.0, step=0.01)
Length = st.number_input("Length (mm)", value=90.0, step=0.01)
Width = st.number_input("Width (mm)", value=34.0, step=0.01)
Height = st.number_input("Height (mm)", value=81.0, step=0.01)
Emissivity = st.number_input("Emissivity", value=0.9, step=0.01)
factor = st.number_input("Factor", value=0.7, step=0.01)

# ================================================================================================================
# Background Calculating For Air Properties
Gravity = 9.81
Thermal_Expansion_Coefficient = 0.00338
Dynamic_viscocity = 0.00001849
Thermal_Diffusivity = 0.00002141
Conductivity_Fluid = 0.02551
Specific_heat_Fluid = 1007
Density_Fluid = 1.184
Kinematic_viscosity = Dynamic_viscocity / Density_Fluid

# Background Calculating for Side
Characteristic_length_side = Height / 1000
Pr_side = (Specific_heat_Fluid * Dynamic_viscocity) / Conductivity_Fluid
Rayleigh_number_side = (
    (Gravity * (1 / (273 + Surface_temperature)) * (Characteristic_length_side**3) * (Surface_temperature - Ambient_temperature))
    / (Kinematic_viscosity**2)
) * Pr_side
Nusselt_number_side = 0.68 + ((0.67 * (Rayleigh_number_side**0.25)) / ((1 + (0.492 / Pr_side) ** (9 / 16)) ** (4 / 9)))
h_side = (Nusselt_number_side * Conductivity_Fluid) / Characteristic_length_side

# Background Calculating for Top
Characteristic_length_top = max(Length / 1000, Width / 1000)
Pr_Top = (Specific_heat_Fluid * Dynamic_viscocity) / Conductivity_Fluid
Rayleigh_number_top = (
    (Gravity * (1 / (273 + Surface_temperature)) * (Characteristic_length_top**3) * (Surface_temperature - Ambient_temperature))
    / (Kinematic_viscosity**2)
) * Pr_Top

value_rayleigh_number = 10000000
if Rayleigh_number_top < value_rayleigh_number:
    Nusselt_number_top = 0.54 * (Rayleigh_number_top ** 0.25)
else:
    Nusselt_number_top = 0.15 * (Rayleigh_number_top ** (1 / 3))
h_top = (Nusselt_number_top * Conductivity_Fluid) / Characteristic_length_top

# Background Calculating for Bottom
Characteristic_length_btm = max(Length / 1000, Width / 1000)
Pr_btm = (Specific_heat_Fluid * Dynamic_viscocity) / Conductivity_Fluid
Rayleigh_number_btm = (
    (Gravity * (1 / (273 + Surface_temperature)) * (Characteristic_length_btm**3) * (Surface_temperature - Ambient_temperature))
    / (Kinematic_viscosity**2)
) * Pr_btm
Nusselt_number_btm = 0.27 * (Rayleigh_number_btm ** 0.25)
h_btm = (Nusselt_number_btm * Conductivity_Fluid) / Characteristic_length_btm

# Background Calculating for Area
TOP_Area = (Length / 1000) * (Width / 1000)
BTM_Area = (Length / 1000) * (Width / 1000)
Side_Area = 2 * ((Length / 1000) * (Height / 1000)) + 2 * ((Width / 1000) * (Height / 1000))

# Background Calculating for Heat Flux
Stefan_Boltzmann_constant = 0.0000000567

Radiation = (
    (Stefan_Boltzmann_constant * Emissivity * ((2 * ((Length / 1000) * (Height / 1000))) + (2 * ((Width / 1000) * (Height / 1000)))) * (((Surface_temperature + 274.15) ** 4) - ((Ambient_temperature + 274.15) ** 4)))
    + (Stefan_Boltzmann_constant * Emissivity * ((2 * (Length / 1000) * (Width / 1000))) * (((Surface_temperature + 274.15) ** 4) - ((Ambient_temperature + 274.15) ** 4)))
)
Convection = (
    (h_side * Side_Area * (Surface_temperature - Ambient_temperature))
    + (h_top * BTM_Area * (Surface_temperature - Ambient_temperature))
    + (h_btm * BTM_Area * (Surface_temperature - Ambient_temperature))
)

# ================================================================================================================
# Streamlit에서 사용될 출력 리스트
Total_power_dissipation = Radiation + Convection
Estimated_power_dissipation = Total_power_dissipation * factor

# 출력 결과를 입력값과 함께 동일한 섹션에 표시
st.header("Results")
st.write(f"**Total Power Dissipation:** {Total_power_dissipation:.4f} W")
st.write(f"  -**Convection:** {Convection:.4f} W")
st.write(f"  -**Radiation:** {Radiation:.4f} W")
st.write(f"**Estimated Power Dissipation with factor :** {Estimated_power_dissipation:.4f} W")
