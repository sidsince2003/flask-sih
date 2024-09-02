# TrueDoc: Document Verification Portal

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Issues and Bug Reports](#issues-and-bug-reports)
- [License](#license)
- [Contact](#contact)

## Introduction

**TrueDoc** is a web-based Document Verification Portal that aims to streamline the process of verifying documents online. The portal offers a secure, user-friendly interface for users to upload, verify, and manage documents. Built with a strong emphasis on security and usability, TrueDoc is an ideal solution for organizations and institutions requiring reliable document verification processes.

This project was designed to be scalable, customizable, and easy to deploy, making it suitable for various environments and use cases.

## Features

- **Secure Document Uploads:** Supports secure document uploads with validation checks.
- **User Authentication:** Secure login and registration system with session management.
- **Dashboard:** A user-friendly dashboard that provides quick access to all the core features.
- **Document Verification:** Robust backend for document verification with a transparent process.
- **Role-Based Access Control:** Different user roles like Admin, Verifier, and User, each with specific permissions.
- **Responsive Design:** Mobile-friendly design for an optimal user experience across devices.
- **Emblem Integration:** Displays India's emblem prominently in the navigation bar to signify official status.

## Technologies Used

- **Frontend:**
  - HTML5
  - CSS3
  - Bootstrap 5
- **Backend:**
  - Python 3.10
  - Flask 2.3.x
- **Database:**
  - MongoDB
- **Deployment:**
  - Vercel for frontend hosting
- **Version Control:**
  - Git & GitHub

## Project Structure

```plaintext
TrueDoc/
│
├── static/                    # Static files (CSS, JS, images)
│   ├── Images/                # Image assets including logos
│   ├── css/                   # Custom CSS files
│   ├── js/                    # Custom JavaScript files
│   
│
├── templates/                 # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Dashboard template
│   ├── login.html             # Login page
│   ├── signup.html            # Signup page
│   
│
├── app.py                     # Main application file
├── config.py                  # Configuration file for environment variables
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
```

## Installation

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or newer installed on your local machine.
- Git installed on your machine.
- An IDE or text editor like VSCode, PyCharm, etc.
- A GitHub account and repository ready for the project.

### Clone the Repository

Clone the TrueDoc repository from GitHub:

```bash
git clone https://github.com/soham2710/sih.git
cd sih
```

#Clone the Repository
Clone the TrueDoc repository from GitHub:

bash
git clone https://github.com/soham2710/sih.git
cd sih

Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies:

bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install Dependencies
Install the required Python packages using pip:

bash
pip install -r requirements.txt

#Running the Application
Configure Environment Variables
Create a .env file in the root directory of your project and add the following:

plaintext
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key


#Initialize the Database
bash

flask db init
flask db migrate -m "Initial migration."
flask db upgrade

# Start the Flask Development Server
bash

flask run

Visit http://127.0.0.1:5000 in your browser to view the application.

# Deployment
Deploying on Vercel
Make sure you have the Vercel CLI installed.
Initialize your Vercel project with vercel init.
Deploy your project using vercel --prod.


# Usage
Accessing the Dashboard
Login using your credentials (or sign up if you haven't).
Use the navigation bar to access different sections of the portal.
Upload and verify documents as per the instructions.
Administrative Tasks
Admins can manage users, view logs, and oversee the document verification process.
