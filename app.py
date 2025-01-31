from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder="templates")

API_KEY = "bd03a81a21c05ea96e2e2372ade3b8c7"
BASE_URL = "http://api.aviationstack.com/v1/flights"

# Function to fetch flight details
def get_flight_details(flight_number):
    params = {"access_key": API_KEY, "flight_iata": flight_number}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            return data["data"][0]  # Return first flight result
    return None

# Function to get an exterior image from Planespotters.net
def get_exterior_image(registration):
    if not registration:
        return None
    return f"https://www.planespotters.net/search?q={registration}"

@app.route("/", methods=["GET", "POST"])
def home():
    flight_data = None
    exterior_img = None

    if request.method == "POST":
        flight_number = request.form.get("flight_number")
        if flight_number:
            flight_data = get_flight_details(flight_number)

            if flight_data:
                registration = flight_data["aircraft"].get("registration")
                exterior_img = get_exterior_image(registration)

                # Debugging Output
                print("\n--- Debugging Info ---")
                print(f"Flight Number: {flight_number}")
                print(f"Registration: {registration}")
                print(f"Exterior Image URL: {exterior_img}")

    return render_template(
        "index.html",
        flight=flight_data,
        exterior_img=exterior_img
    )

if __name__ == "__main__":
    app.run(debug=True)