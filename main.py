from datetime import datetime
import requests

NX_APP_ID = "a0aa03e1"
NX_API_KEY = "XXXXXXXXXXX"
NX_BASE_URL = "https://trackapi.nutritionix.com"
EXERCISE_API = "/v2/natural/exercise"
SHEETY_BASE_URL = "https://api.sheety.co"
WORKOUT_TRACKER_API = "/8e7a7dc2a8849028d5c9c103dd334896/workoutTracker/workouts"
SHEETY_API_KEY = "XXXXXX"

# * --------- ask user for the exercises they did ------------
exercise_input = input("Which exercise did you complete?")

user_data = {
    "query": exercise_input,
    "gender": "male",
    "weight_kg": 65,
    "height_cm": 177,
    "age": 29
}

nx_headers = {
    "x-app-id": NX_APP_ID,
    "x-app-key": NX_API_KEY,
    "Content-Type": "application/json"
}

nx_url = NX_BASE_URL + EXERCISE_API


# * --------- get exercise data from NL model ------------
print(f" [+] posting data to exercise api...:\n")

response = requests.post(url=nx_url, json=user_data, headers=nx_headers)

# get useful request errors when they occur
response.raise_for_status()

data = response.json()
print(f" [+] response data:\n {data}")

# * --------- store exercise data to google sheet ------------
now = datetime.now()
sheet_url = SHEETY_BASE_URL + WORKOUT_TRACKER_API
sheety_headers = {
    "Authorization": f"Bearer {SHEETY_API_KEY}"
}

for exercise in data["exercises"]:
    row_data = {
        "workout": {
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M:%S"),
            "exercise": exercise["name"].capitalize(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }

    }

    print(f" [+] posting data to sheety api...:\n")

    response = requests.post(
        url=sheet_url, json=row_data, headers=sheety_headers)
    response.raise_for_status()
    data = response.json()
    print(f" [+] response data:\n {data}")
