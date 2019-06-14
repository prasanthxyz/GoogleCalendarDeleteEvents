from __future__ import print_function

# CONFIGURATION SECTION
CALENDAR_ID = 'primary'
FILENAME = 'events.csv'
# CONFIGURATION SECTION END

import sys
import csv
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    if len(sys.argv) == 1:
        printEvents(service)
    elif len(sys.argv) == 2 and sys.argv[1] in ['--delete', '--print']:
        if sys.argv[1] == '--delete':
            deleteEvents()
        elif sys.argv[1] == '--print':
            printEvents(service, printToConsole=True)
    else:
        print('Usage:')
        print('./' + sys.argv[0] + ' : Writes all the events into ' + FILENAME)
        print('./' + sys.argv[0] + ' --print : Prints all the events to console, and writes them into ' + FILENAME)
        print('./' + sys.argv[0] + ' --delete : Deletes all the events currently in ' + FILENAME)

def printEvents(service, printToConsole=False):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting all the events in the calendar')
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now).execute()
    events = events_result.get('items', [])

    lines = [['Event ID', 'Event Summary', 'Event Date']]

    if not events:
        print('No upcoming events found.')
    else:
        if printToConsole:
            print(', '.join(lines[0]))
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            line = [event['id'], event['summary'], start]
            lines.append(line)
            if printToConsole:
                print(', '.join(line))
            with open(FILENAME, 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
        print('All events data are written into ' + FILENAME)
        print('Filter manually (delete the rows you want to keep) and re-run with --delete flag')

def deleteEvents():
    print('WARNING: THIS WILL DELETE YOUR CALENDAR EVENTS IN ' + FILENAME)
    user_input = raw_input('Are you sure to continue? (y/n) : ')
    if user_input not in ['y', 'Y']:
        print('Deletion cancelled.')
        return

    with open(FILENAME, 'r') as readFile:
        reader = csv.reader(readFile)
        lines = list(reader)
        print(', '.join(lines[0]))
        for event in lines[1:]:
            eventId = event[0].strip()
            print('deleting ' + ', '.join(event[1:]))
            try:
                service.events().delete(calendarId=CALENDAR_ID, eventId=eventId).execute()
            except Exception, e:
                print('Error:', e)

if __name__ == '__main__':
    main()
