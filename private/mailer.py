# Attempting to send mail at the correct times.

import time
from datetime import datetime
from gluon.tools import Mail

mail = Mail()

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'dontforgetyourevent@gmail.com'
mail.settings.login = 'dontforgetyourevent@gmail.com:web2pyucsc'

def phoneProviderList(phonenumber):

    listOfNumbers = []
    listOfNumbers.append(phonenumber + "@text.wireless.alltel.com") #Alltel
    listOfNumbers.append(phonenumber + "@text.att.net")             #AT&T
    listOfNumbers.append(phonenumber + "@sms.mycricket.com")        #Cricket
    listOfNumbers.append(phonenumber + "@messaging.sprintpcs.com")  #Sprint
    listOfNumbers.append(phonenumber + "@page.nextel.com")          #Nextel
    listOfNumbers.append(phonenumber + "@tmomail.net")              #T-Mobile
    listOfNumbers.append(phonenumber + "@email.uscc.net")           #U.S. Cellular
    listOfNumbers.append(phonenumber + "@vtext.com")                #Verizon
    return listOfNumbers

while True: # inf loop

    currentMin = datetime.now().minute
    currentHour = datetime.now().hour

    if currentHour < 10:
    	currentHourString = "0" + str(currentHour)
    else:
    	currentHourString = str(currentHour)

    # Current Date YYYY-MM-DD

    currentDate = datetime.now().date

    print(":re")

    # Current Time HH:MM:00


    currentTime = currentHourString + ":" + str(currentMin) + ":00"

    print(currentTime)

    rows = db((db.alarm.reminder_date == currentDate) & (db.alarm.reminder_time==currentTime)).select()

    for row in rows:
        theList = phoneProviderList(row.phone_number)
        print(row.phone_number + " -- " + str(row.reminder_date) + " -- " + str(row.reminder_time) + " -- " + row.reminder_message)

        mail.send(to=theList,subject="Don't Forget!",message=row.reminder_message)

    time.sleep(50) # check every 50s