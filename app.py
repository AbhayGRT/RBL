import streamlit as st
from s3 import upload_image_to_s3_with_date_structure
import cv2
import pytesseract
from mindee import extract_data_and_create_dataframe as mindee_extract
from veryfi import extract_data_and_create_dataframe as veryfi_extract
from base641 import extract_data_and_create_dataframe as base64_extract
from inbuilt_ocr import extract_cheque_details as inbuilt_ocr_extract
import pandas as pd
import datetime

# Title
st.title("Cheque Data Extraction App")

# Upload Image
uploaded_image = st.file_uploader("Upload a Cheque Image", type=["jpg", "png", "jpeg"])

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Cheque Image", use_column_width=True)
    st.write("Image uploaded successfully!")

    # Store the uploaded image in S3 and get the link
    s3_link = upload_image_to_s3_with_date_structure(uploaded_image, s3_bucket='chequeimages', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

    # Offer options to extract data
    ocr_option = st.selectbox("Select OCR Method", ("Inbuilt OCR", "Mindee", "Veryfi", "Base64"))

    # Check which option was selected
    if ocr_option == "Inbuilt OCR":
        # Load the check image and convert it to grayscale
        image = cv2.imdecode(uploaded_image.read(), cv2.IMREAD_COLOR)
        cheque_information = pytesseract.image_to_string(image)
        bank_name_list = ['State Bank Of India', 'ICICI Bank', 'HDFC Bank', 'Axis Bank', 'Kotak Mahindra Bank']
        cheque_details_df = inbuilt_ocr_extract(cheque_information, bank_name_list)

    elif ocr_option == "Mindee":
        # Use the link to extract data with the Mindee API
        api_key = "YOUR_MINDEE_API_KEY"
        cheque_details_df = mindee_extract(api_key, s3_link)

    elif ocr_option == "Veryfi":
        # Use the link to extract data with the Veryfi API
        api_key = "YOUR_VERYFI_API_KEY"
        cheque_details_df = veryfi_extract(api_key, s3_link)

    elif ocr_option == "Base64":
        # Use the link to extract data with the Base64 API
        api_key = "YOUR_BASE64_API_KEY"
        cheque_details_df = base64_extract(api_key, s3_link)

    # Display extracted data
    st.write("Extracted Cheque Data:")
    st.write(cheque_details_df)

    # Option to save the data
    if st.button("Save Data as CSV"):
        # Get the current date in the format "date_month_year"
        today = datetime.date.today()
        date_folder = today.strftime('%d_%m_%Y')
        csv_file_path = f'{date_folder}.csv'

        # Ask the user if they want to save the file
        user_input = st.text_input(f"Do you want to save the DataFrame as {csv_file_path}? (yes/no)")

        if user_input.lower() == "yes":
            cheque_details_df.to_csv(csv_file_path, index=False)
            st.write(f'DataFrame saved as CSV file: {csv_file_path}')
        else:
            st.write('File not saved.')

