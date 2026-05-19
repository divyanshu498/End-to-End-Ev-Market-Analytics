import pandas as pd
import requests

# SODA2 API Endpoint for Washington State EV Population Data
URL = "https://data.wa.gov/resource/f6w7-q2d2.json"

# setting a high limit to bypass the default limit of 1000 restriction.
# Fatching up to 300000 rows to ensure we get the complete dataset.
params = {
    "$limit": 300000
}
print("Fetching data from API...(This might take a minutes or two depending on network speed)")

# Execute the API GET request
response = requests.get(URL, params=params)

# Check if the request was successful (HTTP status code 200 means ok)
if response.status_code == 200:
    # Extract JSON payload from the response
    data = response.json()
    # Convert the JSON data into a pandas DataFrame
    df = pd.DataFrame(data)
    print(f"Data Successfully fetched! Total rows: {len(df)}")

    #Display the columns names for verification
    print("Columns in the dataset:")
    print(df.columns)

    # Save the raw data locally as a CSV file to avoid repeated API calls during development
    df.to_csv("ev_data_raw.csv", index=False)
    print("data saved successfully as 'ev_data_raw.csv'. Ready for data cleaning!")

else:
    # Handle potoential API errors gracefully
    print(f"Failed to fetch data. Error Code: {response.status_code}")