# Attempting to send mail at the correct times.

import time
from datetime import datetime

while True: # inf loop 

    currentMin = datetime.now().minute
    currentHour = datetime.now().hour

    currentTime = str(currentHour) + ":" + str(currentMin) + ":00"

    rows = db(db.alarm.reminder_time==currentTime).select()

    for row in rows:
        theList = phoneProviderList(row.phone_number)

        mail.send(to=theList,
             subject="Don't Forget!",
             message=row.reminder_message)

    time.sleep(60) # check every 60s
