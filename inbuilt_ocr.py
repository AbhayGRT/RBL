
import cv2
import pytesseract
import re
import pandas as pd

def extract_cheque_details(cheque_information, bank_name_list):
    cheque_details = {}

    # Extract the validity period.
    validity_period_match = re.search(r'VALID (FOR|UPTO) (\d+) (MONTHS|MONTHS ONLY)', cheque_information)
    if validity_period_match:
        cheque_details['Validity Period'] = [validity_period_match.group(2)]

    # Extract the cheque date.
    cheque_date_match = re.search(r'\d{2}-\d{2}-\d{2}', cheque_information)
    if cheque_date_match:
        cheque_details['Cheque Date'] = [cheque_date_match.group(0)]

    # Extract the payee name.
    payee_name_match = re.search(r'PAY (.*) AT', cheque_information)
    if payee_name_match:
        cheque_details['Payee Name'] = [payee_name_match.group(1)]

    # Extract the amount in digits.
    amount_in_digits_match = re.search(r'(RUPEES|only) (\d+(,\d+)*)(\.\d{2})?', cheque_information)
    if amount_in_digits_match:
        cheque_details['Amount in Digits'] = [amount_in_digits_match.group(2).replace(',', '')]

    # Extract the account number.
    account_number_match = re.search(r'(\d+(,\d+)*) A/c. No.', cheque_information)
    if account_number_match:
        cheque_details['Account Number'] = [account_number_match.group(1).replace(',', '')]

    # Extract the bank name.
    bank_name_match = re.search('|'.join(bank_name_list), cheque_information)
    if bank_name_match:
        cheque_details['Bank Name'] = [bank_name_match.group(0)]

    # Extract the MICR code.
    micr_code_match = re.search(r'IFS CODE: ([A-Z0-9]+)', cheque_information)
    if micr_code_match:
        cheque_details['MICR Code'] = [micr_code_match.group(1)]

    return pd.DataFrame(cheque_details)

bank_name_list = ['State Bank Of India', 'ICICI Bank', 'HDFC Bank', 'Axis Bank', 'Kotak Mahindra Bank']

# Load the check image and convert it to grayscale
# s3_url = cv2.imread("/home/abhay/Documents/cheque.png")
s3_url = "path"
gray_image = cv2.cvtColor(s3_url, cv2.COLOR_BGR2GRAY)

# Apply additional image preprocessing techniques
gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
gray_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

cheque_information = pytesseract.image_to_string(gray_image)

cheque_details_df = extract_cheque_details(cheque_information, bank_name_list)

print(cheque_details_df)
