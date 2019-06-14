# GoogleCalendarDeleteEvents
Batch delete selected events in a google calendar after manual filtering

Installation and Configuration
==============================
1. Install the required packages: <br/>```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
2. Enable the Google Calendar API (step 1 in https://developers.google.com/calendar/quickstart/python) and download the credentials.json file into the same directory as the code
3. Run the code and proceed to authenticate the application (I've copy pasted the same code from the above url i.e. haven't tampered with the auth process)
4. Edit the configuration section to put calendar ID (get it from google calendar settings page) and input/output csv filename

Usage
=====
./googleCalApi.py : Writes all the events into the csv file
./googleCalApi.py --print : Prints all the events to console, and writes them into the csv file
./googleCalApi.py --delete : Deletes all the events currently in the csv file
