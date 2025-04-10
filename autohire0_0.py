# -*- coding: utf-8 -*-
"""AutoHire0.0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17I4tf99JJGzroVwOB2egWDg_4Mu5GhMP
"""

from ipywidgets import Dropdown
from IPython.display import display
import pandas as pd
import PyPDF2
from google.colab import files

# --- Load Job Titles from CSV ---
try:
    df_jobs = pd.read_csv('/content/job_description.csv', encoding='latin-1') # Adjust encoding if needed
except Exception as e:
    print(f"Error loading job description CSV: {e}")
    print("Please ensure the file path is correct and try different encodings.")
    df_jobs = pd.DataFrame()

unique_job_titles = []
if not df_jobs.empty:
    if 'Job Title' in df_jobs.columns:
        unique_job_titles = df_jobs['Job Title'].unique().tolist()
    else:
        print("Warning: 'Job Title' column not found in job_description.csv.")

# --- Upload PDF and Extract Text ---
uploaded_pdf = files.upload()
pdf_filename = list(uploaded_pdf.keys())[0] if uploaded_pdf else None
pdf_text = None

if pdf_filename:
    print(f"Uploaded file: {pdf_filename}")

    def extract_text_from_pdf(pdf_path):
        text = ""
        try:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
        except FileNotFoundError:
            print(f"Error: PDF file not found at {pdf_path}")
            return None
        except Exception as e:
            print(f"An error occurred while reading the PDF: {e}")
            return None
        return text

    pdf_text = extract_text_from_pdf(pdf_filename)

    if pdf_text:
        print("Text extraction from PDF successful.")
    else:
        print("Text extraction from PDF failed.")
else:
    print("No PDF file uploaded.")

# --- Create and Display Dropdown for Job Position ---
selected_position = None
if unique_job_titles:
    dropdown = Dropdown(
        options=unique_job_titles,
        description='Select Position:',
        disabled=False,
    )
    display(dropdown)

    # To get the selected value, you need to run the next cell *after* selecting.
    # The value will be stored in the 'selected_position' variable.
    # print("Please select a position from the dropdown above and then run the next cell.")
else:
    print("No job titles available to create the dropdown.")

if 'dropdown' in locals():
    selected_position = dropdown.value
    print(f"\nYou have selected the position: {selected_position}")

df_jobs=df_jobs.iloc[:, :2].copy()
df_jobs.head()

pdf_text

selected_position

apikey="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"

import os
import json
from groq import Groq

# --- Get Job Description for Selected Position ---
selected_job_description = None
if df_jobs is not None and not df_jobs.empty and 'Job Title' in df_jobs.columns and 'Job Description' in df_jobs.columns and selected_position:
    job_row = df_jobs[df_jobs['Job Title'] == selected_position].iloc[0]
    selected_job_description = job_row['Job Description']

else:
    print("Error: Could not retrieve job description.")

# --- Prepare Prompt for Groq ---
if pdf_text and selected_job_description:
   prompt = f"""
    Compare the following job description with the provided resume text.

    Job Description:
    {df_jobs}

    Resume Text:
    {pdf_text}
    applying for role:
    {selected_position}

    Identify the matching skills between the resume and the job description.
    Explain why this candidate is a good fit for this role based on the comparison (provide a "reasons_to_hire" description).
    Provide an overall numerical percentage score (0-100) indicating how well the resume matches the job description (label this as "match_score").
    return only in the Json formate

    Return your response as a JSON object with the following keys:
    - name:''
    -"email":""
    - "phone_number": ""
    -"applied for the postion":""
    - "matching_skills": ["skill1", "skill2", ...]
    - "reasons_to_hire": "A concise explanation..."
    - "match_score": any number



    give only json as the output
    """

    # --- Call Groq LLM API (Streaming) ---
GROQ_API_KEY = "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"# Ensure you have set your API key
if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY environment variable not set.")
else:
        client = Groq(api_key=GROQ_API_KEY)

        try:
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7, # Adjust temperature for creativity vs. determinism
                max_completion_tokens=1024,
                top_p=0.95,
                stream=True,
                stop=None,
            )

            print("\n--- Groq LLM Response (Streaming) ---")
            llm_response = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                print(content, end="")
                llm_response += content
            print() # Add a newline after the streaming is complete

            # --- Basic Attempt to Parse (Streaming might make JSON parsing harder) ---
            # Depending on how the LLM streams, parsing JSON directly might be unreliable.
            # You might need to wait for the full response if you strictly need JSON.
            # For now, let's just print the full response.

            # If you need structured output, you might need to adjust the prompt
            # and potentially process the full llm_response string after streaming.

        except Exception as e:
            print(f"Error calling Groq API: {e}")

        else:
          print("Error: Resume text or selected job description is not available.")

llm_response

import sqlite3
import json
import re

# Assuming llm_response is the variable containing the Groq LLM's response
print("--- Debug: Content of llm_response ---")
print(repr(llm_response))
print("--- End Debug: Content of llm_response ---")

# Extract JSON from code block, even if it's not tagged as ```json
json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', llm_response, re.DOTALL)
if json_match:
    llm_output_json = json_match.group(1)
    print("--- Debug: Extracted JSON Content ---")
    print(repr(llm_output_json))
    print("--- End Debug: Extracted JSON Content ---")
else:
    # Fallback: strip any backticks and try to parse whatever's inside
    print("Warning: Could not find JSON markers. Trying raw response cleanup...")
    llm_output_json = llm_response.strip('`').strip()

if llm_output_json:
    print("llm_output_json is not empty")
    try:
        data = json.loads(llm_output_json)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Problematic JSON String: {repr(llm_output_json)}")
        data = {}

    if data:
        # Extract the values from the dictionary
        name = data.get("name")
        email = data.get("email")
        phone_number = data.get("phone_number")
        applied_position = data.get("applied for the postion")  # Keep the typo if it's consistent in input
        matching_skills = json.dumps(data.get("matching_skills"))  # Store as JSON string
        reasons_to_hire = data.get("reasons_to_hire")
        match_score = data.get("match_score")

        # Connect to the SQLite database
        conn = sqlite3.connect('job_applications.db')
        cursor = conn.cursor()

        try:
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    name TEXT,
                    email TEXT PRIMARY KEY,
                    phone_number TEXT,
                    applied_position TEXT,
                    matching_skills TEXT,
                    reasons_to_hire TEXT,
                    match_score REAL
                )
            """)

            # Insert or replace (in case of re-run with same email)
            cursor.execute("""
                INSERT OR REPLACE INTO applications
                (name, email, phone_number, applied_position, matching_skills, reasons_to_hire, match_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, email, phone_number, applied_position, matching_skills, reasons_to_hire, match_score))

            conn.commit()
            print("✅ Data successfully stored in 'job_applications.db' with 'email' as primary key.")

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            conn.rollback()

        finally:
            conn.close()
    else:
        print("Parsed JSON data is empty.")
else:
    print("The llm_output_json variable is empty. No data to store.")

import sqlite3

def sort_by_match_score_descending(database_path, table_name):
    """Retrieves all data from a table sorted by match_score in descending order.

    Args:
        database_path (str): The path to the SQLite database file.
        table_name (str): The name of the table to retrieve data from.

    Returns:
        list: A list of tuples, where each tuple represents a row sorted by match_score (descending),
              or None if an error occurs.
    """
    conn = None
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Execute the SELECT query with ORDER BY clause
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY match_score DESC")
        sorted_data = cursor.fetchall()
        return sorted_data

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    finally:
        if conn:
            conn.close()

# --- Example Usage ---
database_file = 'job_applications.db'  # Replace with your database file path
table_to_sort = 'applications'        # Replace with your table name

sorted_results = sort_by_match_score_descending(database_file, table_to_sort)

if sorted_results:
    print(f"Data from table '{table_to_sort}' sorted by match_score (descending):")
    # Print the column names for better readability
    conn_temp = sqlite3.connect(database_file)
    cursor_temp = conn_temp.cursor()
    cursor_temp.execute(f"PRAGMA table_info({table_to_sort})")
    columns_info = cursor_temp.fetchall()
    column_names = [info[1] for info in columns_info]
    print(column_names)
    conn_temp.close()

    for row in sorted_results:
        print(row)
else:
    print(f"Could not retrieve and sort data from table '{table_to_sort}'.")

import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import random
import os  # For creating directories

def get_top_n_applicants(database_path, table_name, n=5):
    """Retrieves the email addresses and names of the top N applicants based on match_score (descending)."""
    conn = None
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT email, name
            FROM {table_name}
            ORDER BY match_score DESC
            LIMIT ?
        """, (n,))
        top_applicants = cursor.fetchall()
        return top_applicants
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def send_interview_schedule_email(recipient_email, recipient_name, interview_time_str, interview_address, sender_email, sender_password):
    """Sends an email with the interview schedule to the applicant."""
    subject = "Your Interview Schedule"
    body = f"""
Dear {recipient_name},

We are pleased to invite you for an offline interview as part of the next stage of our hiring process.

Your interview has been scheduled for:
Date: {interview_time_str.split(' ')[0]}
Time: {interview_time_str.split(' ')[1]} Indian Standard Time (IST)
Address: {interview_address}

Please arrive 15 minutes prior to your scheduled time.

If you have any questions or need to reschedule, please contact us as soon as possible.

Thank you for your continued interest.

Sincerely,
[Your Company Name]
"""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Interview schedule sent successfully to: {recipient_email} at {interview_time_str} IST")
    except Exception as e:
        print(f"Error sending interview schedule to {recipient_email}: {e}")

DATABASE_FILE = '/content/job_applications.db'  
TABLE_NAME = 'applications'
TOP_N = 5
INTERVIEW_DATE_OFFSET_DAYS = 10

INTERVIEW_START_TIME = datetime(2025, 4, 18, 10, 0, 0)
INTERVIEW_TIME_DIFFERENCE_MINUTES = 30
INTERVIEW_ADDRESS = "XYZ Corp, Innovation Park, Bengaluru"
SENDER_EMAIL = 'nouse200426@gmail.com' 
SENDER_PASSWORD = 'wwvd rvcx lmrg ffng'  

# --- Main Execution ---
if __name__ == "__main__":
    top_applicants_data = get_top_n_applicants(DATABASE_FILE, TABLE_NAME, TOP_N)

    if top_applicants_data:
        print(f"Top {TOP_N} applicants: {top_applicants_data}")
        interview_time = INTERVIEW_START_TIME
        for i, (email, name) in enumerate(top_applicants_data):
            interview_time_str = interview_time.strftime("%Y-%m-%d %I:%M%p")
            send_interview_schedule_email(email, name, interview_time_str, INTERVIEW_ADDRESS, SENDER_EMAIL, SENDER_PASSWORD)
            interview_time += timedelta(minutes=INTERVIEW_TIME_DIFFERENCE_MINUTES)
    else:
        print("Could not retrieve top applicant data.")

