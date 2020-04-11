Copyright 2020 Jacques Parker 
code@judyandjacques.com

I got tired of repeatedly checking the Giant Eagle grocery store for a pickup slot for curbside groceries.

Please feel free to use this script to help you RESPONSIBLY schedule your curbside pickup.

This is my first selenium project and should probably not be used as a template for more complex projects. 
This is meant to be a simple adhoc script developed for this very specific website.  No unit test, etc.

GiantEagle.py - Main script

GiantEagle.json - This is the properties file that contains credentials for Giant Eagle and Twilio.  This
will need to be setup before trying to run the script

GiantEagle.disable - If this file exists the script will exist immediately.  This is meant to keep the script
from running once an alert has been sent out.  e.g. if run by a cron job.

TwilioSendText.py - Send test text using the json property settings.

CreateJSON.py - Create json property file with all of the expected fields.

Required libraries - selenium, twilio

Currently written to use the chrome driver (version 59+ to use headless mode).  
Download can be found here https://chromedriver.chromium.org/downloads

