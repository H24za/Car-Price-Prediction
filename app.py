import streamlit as st
import requests

st.set_page_config(page_title="Car Price Prediction", layout="centered")
st.title("🚗 Car Price Prediction")
st.write("أدخل بيانات السيارة ثم اضغط على زر التنبؤ:")

# --- Form Inputs ---
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        Levy = st.number_input("Levy (0 if none)", min_value=0, value=500)
        Manufacturer = st.text_input("Manufacturer", value="Toyota")
        Category = st.text_input("Category", value="Sedan")
        Leather_interior = st.selectbox("Leather Interior", ["Yes", "No"])
        Engine_volume = st.number_input("Engine Volume", min_value=0.0, value=2.0, step=0.1)
        Mileage = st.number_input("Mileage", min_value=0, value=120000)
        Gear_box_type = st.text_input("Gear Box Type", value="Automatic")
        Wheel = st.text_input("Wheel", value="Left")
        Color = st.text_input("Color", value="White")
    with col2:
        Prod_year = st.number_input("Production Year", min_value=1900, max_value=2025, value=2015)
        Model = st.text_input("Model", value="Camry")
        Fuel_type = st.text_input("Fuel Type", value="Petrol")
        Cylinders = st.number_input("Cylinders", min_value=1, value=4)
        Drive_wheels = st.text_input("Drive Wheels", value="Front")
        Airbags = st.number_input("Airbags", min_value=0, value=6)
    submitted = st.form_submit_button("Predict")

# --- Prediction Logic ---
if submitted:
    sample_data = {
        "Levy": Levy,
        "Manufacturer": Manufacturer,
        "Model": Model,
        "Prod_year": Prod_year,
        "Category": Category,
        "Leather_interior": Leather_interior,
        "Fuel_type": Fuel_type,
        "Engine_volume": Engine_volume,
        "Mileage": Mileage,
        "Cylinders": Cylinders,
        "Gear_box_type": Gear_box_type,
        "Drive_wheels": Drive_wheels,
        "Wheel": Wheel,
        "Color": Color,
        "Airbags": Airbags
    }
    # Try both ports (8000, 8001)
    for port in [8000, 8001]:
        try:
            url = f"http://127.0.0.1:{port}/predict/"
            response = requests.post(url, json=sample_data, timeout=5)
            if response.status_code == 200:
                st.success(f"Prediction: {response.json()['prediction']}")
                break
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            if port == 8001:
                st.error("❌ Could not connect to FastAPI server on ports 8000 or 8001. تأكد أن السيرفر يعمل.")
