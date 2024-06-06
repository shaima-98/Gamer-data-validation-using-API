import requests
import csv
import pandas as pd
import datetime
import re

# Get the current date in the desired format
#To get a new file with the current date when it is required to run everyday
current_date = datetime.datetime.now()
current_date_str = current_date.strftime("%B-%d")

# Define the CSV file path
csv_file_1 = f"C:/path/to/your/directory/Game_{current_date_str}.csv"

final_df = pd.DataFrame()
final_data = []

# Prompt user for space-separated account numbers
user_input = input("Enter space-separated account numbers: ")
accounts = re.split(r'\n|\s+', user_input.strip())
unique_accounts_input = []

# Process each account to ensure uniqueness
for x in accounts:
    if x not in unique_accounts_input: 
        lower_email = x.lower()
        unique_accounts_input.append(lower_email)
print(unique_accounts_input)

# API endpoint and headers (replace with your own endpoint and token)
api_url = "https://api.yourservice.com/users"  # Replace with the actual API URL
api_token = "YOUR_API_TOKEN"  # Replace with your actual API token

for email in unique_accounts_input:
    
    headers = {
        "Authorization": f"Bearer {api_token}"  # Use Bearer token for authorization
    }
    params = {
        "email": email
    }

    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        raw_data = response.json().get('result', [])
        if raw_data:
            json_data = raw_data[0]
            if json_data:
                trophies_data = json_data.get('trophies', 0)
                xp_data = json_data.get('xp', 0)
                trophies_validation = lambda x: "Validated" if x > 500 else "Not Validated"  # validation
                validation_result = trophies_validation(trophies_data)

                final_data.append({
                    'Email': email,
                    'trophies': trophies_data,
                    'xp': xp_data,
                    'validation': validation_result
                })
                print(f"Data received for: {email}")
            else:
                print(f"No data found in the 'result' field for {email}")
                final_data.append({
                    'Email': email,
                    'trophies': '',
                    'xp': '',
                    'validation': 'No data'
                })
        else:
            print(f"List is empty for {email}")
            final_data.append({
                'Email': email,
                'trophies': '',
                'xp': '',
                'validation': 'No data'
            })
    else:
        print("Error in response")
    
# Convert final data to DataFrame
final_df = pd.DataFrame(final_data)    

# Save the DataFrame to a CSV file
with open(csv_file_1, mode="a", newline='') as csv_file:
    final_df.to_csv(csv_file, index=False, header=csv_file.tell() == 0)
