import streamlit as st
import pandas as pd
import numpy as np

def convert_units(value, from_unit, to_unit, conversion_dict):
    """
    Convert units based on a predefined conversion dictionary.
    :param value: Numeric value to convert
    :param from_unit: Unit to convert from
    :param to_unit: Unit to convert to
    :param conversion_dict: Dictionary containing conversion rates
    :return: Converted value
    """
    if from_unit in conversion_dict and to_unit in conversion_dict[from_unit]:
        return value * conversion_dict[from_unit][to_unit]
    else:
        return None

# Defining the conversion factors for different unit types
conversion_factors = {
    "Length": {
        "meters": {"kilometers": 0.001, "miles": 0.000621371, "feet": 3.28084},
        "kilometers": {"meters": 1000, "miles": 0.621371, "feet": 3280.83},
        "miles": {"meters": 1609.34, "kilometers": 1.60934, "feet": 5280},
        "feet": {"meters": 0.3048, "kilometers": 0.0003048, "miles": 0.0001893940}
    },
    "Weight": {
        "kilograms": {"grams": 1000, "pounds": 2.20462},
        "grams": {"kilograms": 0.001, "pounds": 0.00220462},
        "pounds": {"kilograms": 0.453594, "grams": 453.572}
    },
    "Temperature": {
        "Celsius": {"Fahrenheit": lambda c: (c * 9/5) + 32, "Kelvin": lambda c: c + 273.15},
        "Fahrenheit": {"Celsius": lambda f: (f - 32) * 5/9, "Kelvin": lambda f: (f - 32) * 5/9 + 273.15},
        "Kelvin": {"Celsius": lambda k: k - 273.15, "Fahrenheit": lambda k: (k - 273.15) * 9/5 + 32}
    }
}

# Streamlit UI
st.set_page_config(page_title="Unit Converter", layout="centered")
st.title("Unit Converter Web App")
st.markdown("### Convert between different units easily and accurately!")
st.divider()

#  selects the type of conversion by user
unit_type = st.selectbox("Select Unit Type", list(conversion_factors.keys()))


col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From Unit", list(conversion_factors[unit_type].keys()))
with col2:
    to_unit = st.selectbox("To Unit", [unit for unit in conversion_factors[unit_type] if unit != from_unit])

# Taking the user inputs the value to convert
value = st.number_input("Enter Value", min_value=0.0, format="%.4f")
converted_value = None  # Initialize converted_value

# Convert the values
if st.button("Convert"):
    if unit_type == "Temperature":
        converted_value = conversion_factors[unit_type][from_unit][to_unit](value)
    else:
        converted_value = convert_units(value, from_unit, to_unit, conversion_factors[unit_type])
    
    if converted_value is not None:
        st.success(f"{value} {from_unit} is equal to {converted_value:.4f} {to_unit}")
        
        # it stores history only if conversion is successful
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append(f"{value} {from_unit} ➡ {converted_value:.4f} {to_unit}")
    else:
        st.error("Conversion not available.")

# here i show the conversion history and its last 5 conversions
if "history" in st.session_state and st.session_state.history:
    st.subheader("Conversion History")
    st.write(st.session_state.history[-5:])  
