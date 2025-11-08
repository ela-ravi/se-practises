# HR One Attendance Automation

## Overview
This project automates the login and attendance marking process for HR One, a human resource management system. The script uses Playwright to interact with the HR One web interface, handling the login flow and attendance marking process automatically.

## Features
- Automated login to HR One portal
- Automatic attendance marking
- Error handling with screenshots for debugging
- Secure credential management using environment variables

## Prerequisites
- Python 3.7+
- Playwright
- Python packages: `python-dotenv`, `playwright`
- A modern web browser (Chromium, Firefox, or WebKit) - will be installed by Playwright

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   If you don't have a requirements.txt, install the packages directly:
   ```bash
   pip install python-dotenv playwright
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install
   ```

4. **Set up environment variables**
   - Create a `.env` file in the project root
   - Add your HR One credentials:
     ```
     HRONE_USERNAME=your_username
     HRONE_PASSWORD=your_password
     ```
   - **Important**: Add `.env` to your `.gitignore` to keep credentials secure

## Usage

1. **Run the script**
   ```bash
   python hrony.py
   ```

2. **The script will:**
   - Open a browser window
   - Navigate to the HR One login page
   - Enter your credentials
   - Mark your attendance
   - Close the browser when done

## Error Handling
- The script takes screenshots when errors occur
- Screenshots are saved in the project directory with descriptive names (e.g., `login_error.png`)
- The browser will remain open for inspection if an error occurs during attendance marking

## Security Note
- Never commit your `.env` file to version control
- The `.gitignore` file is pre-configured to exclude sensitive files

## License
[Specify your license here, e.g., MIT, Apache 2.0, etc.]
