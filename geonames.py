import requests

# API endpoint
url = "http://api.geonames.org/findNearbyPostalCodesJSON?country=US&radius=1&username=lihuedon&postalcode="


def get_zip_data(zip="98225"):
    urlzip = url+zip
    # Headers (if needed, for example, for authentication)
    headers = {
        "Authorization": "lihuedon",
        "Content-Type": "application/json"
    }
    data = {}
    try:
        # Send GET request
        response = requests.get(urlzip, headers=headers)
        # Check for successful response
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            # print("Data retrieved:", data)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print("An error occurred:", e)
    return data

