Hong Kong Leisure and Cultural Services Department (LCSD) Facility Booking Bot
This project is a Python script that automates the process of logging into the Hong Kong Leisure and Cultural Services Department (LCSD) SmartPLAY system and booking a facility. It uses the Selenium library to interact with the website.

Prerequisites
Python 3.6+
Google Chrome browser
Installation
Step 1: Clone the Repository
sh
複製程式碼
git clone https://github.com/yourusername/lcsd-booking-bot.git
cd lcsd-booking-bot
Step 2: Set Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

sh
複製程式碼
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Step 3: Install Dependencies
Install the necessary Python libraries using pip.

sh
複製程式碼
pip install selenium
Step 4: Download ChromeDriver
Download the ChromeDriver that matches your version of Chrome from here.

Extract the downloaded file and place the chromedriver executable in a directory included in your system's PATH or specify the path to the executable in the script.

Usage
Update the script with your SmartPLAY username, password, and desired booking details (date, time, and venue).

Run the script:

sh
複製程式碼
python lcsd_booking_bot.py
Script Overview
login(username, password)
Logs into the SmartPLAY system using the provided username and password.

navigate_to_facility()
Navigates to the facility booking page.

book_venue(date, time, venue)
Books the specified facility on the specified date and time.

Example
Update the following variables in the script with your credentials and booking details:

python
複製程式碼
username = 'your_username'
password = 'your_password'
date = '2024-07-10'
time = '10:00'
venue = '某体育馆'
Run the script:

sh
複製程式碼
python lcsd_booking_bot.py
Notes
Ensure that your Chrome browser is up to date and that the version of ChromeDriver matches your Chrome browser version.
If the website structure changes, you may need to update the XPath or other selectors in the script.
Use this script responsibly and in accordance with the terms of service of the LCSD SmartPLAY system.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Selenium
ChromeDriver
Feel free to contribute to this project by opening issues or submitting pull requests. Your feedback and improvements are welcome!

