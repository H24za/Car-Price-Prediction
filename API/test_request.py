import requests
from requests.exceptions import RequestException

# Probe /health to find a running server. Try ports 8001 then 8000.
base_candidates = ["http://127.0.0.1:8001", "http://127.0.0.1:8000"]
base = None
for b in base_candidates:
    try:
        r = requests.get(f"{b}/health", timeout=1)
        if r.ok:
            base = b
            break
    except RequestException:
        continue

if base is None:
    print('No running server found on ports 8001 or 8000. Start the server first.')
    raise SystemExit(1)

url = f"{base}/predict/"

# مثال بيانات (لازم تعدلها تناسب بياناتك الفعلية)
sample_data = {
    "Levy": 500,
    "Manufacturer": "Toyota",
    "Model": "Camry",
    "Prod_year": 2015,
    "Category": "Sedan",
    "Leather_interior": "Yes",
    "Fuel_type": "Petrol",
    "Engine_volume": 2.0,
    "Mileage": 120000,
    "Cylinders": 4,
    "Gear_box_type": "Automatic",
    "Drive_wheels": "Front",
    "Wheel": "Left",
    "Color": "White",
    "Airbags": 6
}

# إرسال الطلب
response = requests.post(url, json=sample_data)

# طباعة النتيجة
if response.status_code == 200:
    print("✅ Prediction:", response.json())
else:
    print("❌ Error:", response.status_code, response.text) 
