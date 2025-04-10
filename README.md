# AutoHire0.0
An intelligent ATS (Applicant Tracking System) that analyzes resumes against job descriptions using Groq's LLaMA language model. This project automates resume screening, shortlisting candidates based on skills and relevance, and sends interview emails to top applicants.


link for accesing the collab
https://colab.research.google.com/drive/17I4tf99JJGzroVwOB2egWDg_4Mu5GhMP?usp=sharing

🚀 <b>Features</b>
📄 Upload and parse resumes (PDF)

🧾 Extract job descriptions from CSV

🤖 Analyze resume vs job description using Groq LLaMA API

✅ Extract key candidate details like name, email, skills, match score, and reasons to hire

🗃️ Store results in an SQLite database

📊 View sorted applicants by match score

📬 Automatically send interview emails to top candidates

🛠️ Tech Stack
Python

PyPDF2 – PDF text extraction

Pandas – CSV handling

SQLite3 – Local database

smtplib – Email sending

ipywidgets – Interactive UI

Groq API (LLaMA) – LLM inference

📂 Project Structure
bash
Copy
Edit
.
├── job_description.csv       # Contains job roles and their descriptions
├── main.ipynb                # Main notebook with entire pipeline
├── resumes/                  # Uploaded resumes
├── database.db               # SQLite DB storing candidate data
└── README.md                 # Project documentation
⚙️ How It Works
Import Required Libraries – Includes PyPDF2, ipywidgets, pandas, sqlite3, smtplib, etc.

Load Job Descriptions – Read job_description.csv and extract unique job titles.

Upload Resume (PDF) – Extract text using PyPDF2.

Select Job Title – User selects the job to apply for via dropdown.

Generate Prompt for Groq API – Combine job description + resume text.

Call Groq's LLaMA API – Returns JSON with name, email, phone, skills, reasons, and score.

Parse JSON Safely – Use regex + json.loads() to cleanly parse the output.

Store in SQLite – Save the parsed result with email as a primary key.

Sort Applicants – Show candidates sorted by match score.

Email Top Candidates – Schedule interviews and send emails using smtplib.

📬 Email Format (Example)
vbnet
Copy
Edit
Subject: Interview Invitation - [Job Title]

Dear [Candidate Name],

Congratulations! Based on your resume analysis, we are pleased to invite you for an interview for the [Job Title] position.

Your interview is scheduled at: [Time Slot].

Best regards,  
HR Team
✅ Requirements
Install all required packages using:

bash
Copy
Edit
pip install pandas PyPDF2 ipywidgets openai sqlite3
Note: You’ll need access to Groq’s API key for LLaMA inference.

📌 Future Improvements
Web version using Django or Flask

Resume feedback & score visualization

Multi-role support and filtering options

Dashboard to monitor applicant pipeline

👨‍💻 Author
Your Name
BE CSE, RNSIT | Samsung Innovation Campus Trainee
LinkedIn | Email
