
import streamlit as st

# Conversion logic for Length, Weight, and Temperature
conversion_factors = {
    "Length": {
        "meters": {"kilometers": 0.001},
        "kilometers": {"meters": 1000}
    },
    "Weight": {
        "kg": {"g": 1000},
        "g": {"kg": 0.001}
    },
    "Temperature": {
        "C": {
            "F": lambda c: (c * 9/5) + 32
        },
        "F": {
            "C": lambda f: (f - 32) * 5/9
        }
    }
}

# page setup
st.set_page_config(page_title="Unit Converter", layout="centered")
st.title("Simple Unit Converter")

unit_type = st.selectbox("Choose type", list(conversion_factors.keys()))
from_unit = st.selectbox("From", list(conversion_factors[unit_type].keys()))
to_unit = st.selectbox("To", [u for u in conversion_factors[unit_type] if u != from_unit])

value = st.number_input("Enter value", min_value=0.0, format="%.4f")
result = None

if st.button("Convert"):
    # temperature uses functions instead of fixed values
    if unit_type == "Temperature":
        result = conversion_factors[unit_type][from_unit][to_unit](value)
    else:
        result = value * conversion_factors[unit_type][from_unit][to_unit]
    
    if result is not None:
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")
        
        # Save last few conversions as history
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append(f"{value} {from_unit} ➡ {result:.4f} {to_unit}")
    else:
        st.error("Conversion not available.")

# Show recent history
if "history" in st.session_state and st.session_state.history:
    st.subheader("Recent Conversions")
    st.write(st.session_state.history[-3:])

