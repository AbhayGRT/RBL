import requests
import json
import pandas as pd
from s3 import upload_image_to_s3_with_date_structure
import datetime

def extract_data_and_create_dataframe(api_key, file_url):
    # Encode headers and payload with 'utf-8'
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.edenai.run/v2/ocr/bank_check_parsing"
    
    # Encode file_url with 'utf-8'
    json_payload = {
        "show_original_response": False,
        "fallback_providers": "mindee",
        "providers": "base64",
        "file_url": file_url
    }
    
    # Send the request
    response = requests.post(url, json=json_payload, headers=headers)
    
    result = json.loads(response.text)
    data = result["base64"]
    
    # Extract relevant data
    extracted_data = data['extracted_data'][0]
    
    # Create a DataFrame
    df = pd.DataFrame({
        'amount': [extracted_data['amount']],
        'amount_text': [extracted_data['amount_text']],
        'bank_address': [extracted_data['bank_address']],
        'bank_name': [extracted_data['bank_name']],
        'date': [extracted_data['date']],
        'memo': [extracted_data['memo']],
        'payer_address': [extracted_data['payer_address']],
        'payer_name': [extracted_data['payer_name']],
        'receiver_address': [extracted_data['receiver_address']],
        'receiver_name': [extracted_data['receiver_name']],
        'currency': [extracted_data['currency']],
        'micr_raw': [extracted_data['micr']['raw']],
        'micr_account_number': [extracted_data['micr']['account_number']],
        'micr_routing_number': [extracted_data['micr']['routing_number']],
        'micr_serial_number': [extracted_data['micr']['serial_number']],
        'check_number': [extracted_data['micr']['check_number']]
    })
    
    return df

# Example usage of the function:
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzVlNTJiOWMtZTc0MS00YWY1LWEzYjQtNzNkNTMzZWQ1ZGE2IiwidHlwZSI6ImFwaV90b2tlbiJ9.dcbAWTSJX03TjS7kjcPIRqHhSt82dwfXGEDyQLloay0"
s3_url = "path"
file_url = upload_image_to_s3_with_date_structure(s3_url)

result_df = extract_data_and_create_dataframe(api_key, file_url)
print(result_df)


# Get the current date in the format "date_month_year"
today = datetime.date.today()
date_folder = today.strftime('%d_%m_%Y')
csv_file_path = f'{date_folder}.csv'

# Ask the user if they want to save the file
user_input = input(f"Do you want to save the DataFrame as {csv_file_path}? (yes/no): ")

if user_input.lower() == "yes":
    result_df.to_csv(csv_file_path, index=False)
    print(f'DataFrame saved as CSV file: {csv_file_path}')
else:
    print('File not saved.')