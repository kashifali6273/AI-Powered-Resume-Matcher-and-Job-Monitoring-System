# Resume Matcher and Job Monitoring System

## Overview
This project is a **Flask-based web application** that helps users find jobs that best match their resumes.  
It provides resume uploading, job scraping, automated job monitoring, AI-powered resume feedback, and watchlist management.  
The application demonstrates practical use of **Natural Language Processing (NLP)**, automation, and real-time job tracking.

---

## Features

### 1. User Authentication
- Secure login and registration using Flask-Login and SQLite.  
- Each user manages their own resumes and monitoring rules.  

### 2. Resume Management
- Upload multiple resumes in PDF format.  
- Select an existing resume from a personal list.  
- Resumes are stored per user with secure file handling.  

### 3. Job Search and Matching
- Search for jobs by entering a job title.  
- Jobs are scraped in real-time from Rozee.pk (extendable to other platforms).  
- Resumes are compared with job descriptions using NLP-based text similarity.  
- Match scores are calculated and displayed.  
- Jobs can be filtered by:
  - Location
  - Minimum match score

### 4. AI-Powered Resume Feedback
- Upload a resume and job description.  
- The system uses Google Gemini API to provide:  
  - A match score  
  - Suggestions on whether to apply  
  - Improvement feedback for the resume  

### 5. Job Monitoring Rules
- Create rules to monitor specific job titles with a chosen resume.  
- System checks for new jobs every 10 minutes in the background.  
- Matching jobs are stored in a **Watchlist**.  
- Jobs in watchlist include the match score and job details.

### 6. Watchlist Management
- View all jobs that matched monitoring rules.  
- Paginated list of watchlist entries.  
- Delete unwanted entries.  

### 7. User Dashboard
- A clean dashboard layout with grid-style buttons.  
- Access to all major features:
  - Job search
  - Auto job monitoring
  - Watchlist
  - Resume feedback
  - Resume-to-job matching
  - Logout  

### 8. Modern UI
- Dark theme with consistent design across pages.  
- Mobile-friendly layouts with collapsible resume lists.  

---

## Technologies Used

- **Backend:** Flask, Python  
- **Frontend:** HTML, CSS (dark theme, responsive design)  
- **Database:** SQLite (Flask SQLAlchemy ORM)  
- **Authentication:** Flask-Login  
- **File Handling:** Secure resume uploads with `werkzeug`  
- **Web Scraping:** Selenium (Rozee.pk job scraping)  
- **NLP Matching:** Resume text vs Job description similarity  
- **AI Integration:** Google Gemini API for feedback and scoring  
- **Background Jobs:** Automated monitoring with scheduled loops  

---

## Installation

### Prerequisites
- Python 3.8+  
- pip (Python package manager)  
- Google Gemini API Key (for AI features)  

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/resume-matcher.git
   cd resume-matcher
