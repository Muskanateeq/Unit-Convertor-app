# import streamlit as st

# # Conversion factors relative to 1 meter.
# # The keys represent the unit names (with abbreviations for clarity).
# conversion_factors = {
#     "Meter (m)": 1,
#     "Foot (ft)": 0.3048,
#     "Mile (mi)": 1609.344,
#     "Inch (in)": 0.0254,
#     "Kilometer (km)": 1000,
#     "Centimeter (cm)": 0.01,
#     "Millimeter (mm)": 0.001,
#     "Micrometer (µm)": 1e-6,
#     "Nanometer (nm)": 1e-9,
#     "Yard (yd)": 0.9144
# }

# def convert_length(value, from_unit, to_unit):
#     """
#     Convert a length from one unit to another.

#     Parameters:
#         value (float): The numeric value to convert.
#         from_unit (str): The unit of the input value.
#         to_unit (str): The unit to convert to.

#     Returns:
#         float: The converted value.
#     """
#     # Get conversion factor for the source and target units
#     factor_from = conversion_factors[from_unit]
#     factor_to = conversion_factors[to_unit]
    
#     # Convert the input value to meters first, then to the target unit
#     value_in_meters = value * factor_from
#     converted_value = value_in_meters / factor_to
#     return converted_value

# def main():
#     st.title("📏 Unit Converter App")
#     st.write("Convert between various length units easily.")

#     # Input for the numerical value
#     value = st.number_input("Enter the value to convert:", value=0.0)
    
#     # List of available units
#     unit_list = list(conversion_factors.keys())
    
#     # Dropdown selectors for units
#     from_unit = st.selectbox("From Unit:", unit_list)
#     to_unit = st.selectbox("To Unit:", unit_list)
    
#     # Perform conversion on button click
#     if st.button("Convert"):
#         result = convert_length(value, from_unit, to_unit)
#         st.success(f"**{value} {from_unit}** is equal to **{result} {to_unit}**")

# if __name__ == "__main__":
#     main()


import streamlit as st
import re

# Conversion factors relative to 1 meter
conversion_factors = {
    "m": 1,
    "ft": 0.3048,
    "mi": 1609.344,
    "in": 0.0254,
    "km": 1000,
    "cm": 0.01,
    "mm": 0.001,
    "µm": 1e-6,
    "nm": 1e-9,
    "yd": 0.9144
}

def convert_length(value, from_unit, to_unit):
    """
    Convert a value from one unit to another using meters as the base.
    """
    factor_from = conversion_factors.get(from_unit)
    factor_to = conversion_factors.get(to_unit)
    if factor_from is None or factor_to is None:
        return None
    value_in_meters = value * factor_from
    converted_value = value_in_meters / factor_to
    return converted_value

def process_user_message(message):
    """
    Process the user's natural language conversion query.
    It supports queries like "5 m to km" or "convert 5 m to km".
    """
    pattern = r"(\d+(?:\.\d+)?)\s*([a-zA-Zµnm]+)\s*(?:to)\s*([a-zA-Zµnm]+)"
    match = re.search(pattern, message.lower())
    if match:
        value = float(match.group(1))
        from_unit = match.group(2)
        to_unit = match.group(3)
        result = convert_length(value, from_unit, to_unit)
        if result is None:
            return "Sorry, one or both units are not supported."
        else:
            return f"{value} {from_unit} is equal to {result:.4f} {to_unit}"
    else:
        return "Please provide your query in the format: <value> <from_unit> to <to_unit>."

def manual_converter():
    st.header("Manual Converter")
    value = st.number_input("Enter the value:", value=0.0)
    unit_list = list(conversion_factors.keys())
    from_unit = st.selectbox("From Unit:", unit_list, index=0)
    to_unit = st.selectbox("To Unit:", unit_list, index=0)
    
    if st.button("Convert"):
        result = convert_length(value, from_unit, to_unit)
        if result is None:
            st.error("Conversion error: Invalid unit.")
        else:
            st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")

def chatbot_converter():
    st.header("🤖 Chatbot Converter")
    st.write("Type your conversion query (e.g., **5 m to km** or **convert 5 m to km**).")
    
    # Initialize chat history if not present
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Use a form to capture input and clear it after submission
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("You:")
        submitted = st.form_submit_button("Send")
        if submitted and user_input:
            bot_response = process_user_message(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", bot_response))
    
    # Display the conversation
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**Bot:** {message}")

def main():
    st.sidebar.title("Navigation")
    mode = st.sidebar.radio("Choose a mode:", ("Manual Converter", "Chatbot Converter"))
    
    st.title("Unit Converter App")
    
    if mode == "Manual Converter":
        manual_converter()
    else:
        chatbot_converter()

if __name__ == "__main__":
    main()
