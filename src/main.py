# Needs to check this URL for changes on the page, then alert me if there is changes.
# https://www.qantas.com/gb/en/travel-info/travel-updates/coronavirus/qantas-international-network-changes/flights-from-london.html

import requests
import argparse
import time
import sys
from bs4 import BeautifulSoup

URL = 'https://www.qantas.com/gb/en/travel-info/travel-updates/coronavirus/qantas-international-network-changes/flights-from-london.html'
ALERT_URL = 'https://maker.ifttt.com/trigger/page_updated/with/key/{key}'
PREV_TEXT = None
REQUEST_FREQUENCY_SECS = 60

# Get the IFTTT key that is passed in on the command line.
IFTTT_KEY = None
parser = argparse.ArgumentParser(description="Checks QANTAS website for updates about repatriation flights from UK to Aus.")
parser.add_argument("-k","--key", help="IFTTT webhook key to trigger alerts using my phone.", required=True)
parser.add_argument("-f","--frequency", help="How often to check the site (in seconds).", default=30, type=int)
args = parser.parse_args()
IFTTT_KEY = args.key
REQUEST_FREQUENCY_SECS = args.frequency
print("Got IFTTT key: {0}".format(IFTTT_KEY))

# Test the IFTTT endpoint to ensure it is valid.
print("Testing IFTTT endpoint...")
iftttTestReq = requests.get("https://maker.ifttt.com/trigger/TEST/with/key/{0}".format(IFTTT_KEY))
if not iftttTestReq.ok:
    sys.exit("IFTTT endpoint did not return OK request.")
print(iftttTestReq.text)

# Start sending requests to QANTAS url.
print("Will check the site every {0} seconds (CTRL + C to exit).".format(args.frequency))
while True:
    r = requests.get(URL)

    # Detect if QANTAS site is not processing requests.
    if not r.ok:
        print("QANTAS site is not returning OK requests.")
        print(r.text)
        time.sleep(REQUEST_FREQUENCY_SECS)
        continue

    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    mainTag = soup.find(lambda tag: tag.name == 'main')
    pageText = mainTag.text

    # Check if the page text has changed.
    if PREV_TEXT != None and PREV_TEXT != pageText:
        print("Changes to QANTAS site detected, sending out alerts.")
        # Trigger our alert by calling a IFTTT endpoint.
        requests.get(ALERT_URL.format(key=IFTTT_KEY))
        continue
    PREV_TEXT = pageText

    # Only send requests at specified frequency.
    print(".", end="", flush=True)
    time.sleep(REQUEST_FREQUENCY_SECS)
    