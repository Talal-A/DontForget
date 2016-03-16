# Attempting to send mail at the correct times.

import time
import datetime
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

    # Current Date YYYY-MM-DD

    currentDate = datetime.datetime.now().date

    print(":re")

    # Current Time HH:MM:00


    currentTime = datetime.datetime.now().time()
    print(currentTime)

    rows = db(db.alarm.reminder_date == currentDate).select()

    for row in rows:

        theList = phoneProviderList(row.phone_number)
        print(row.phone_number + " -- " + str(row.reminder_date) + " -- " + str(row.reminder_time) + " -- " + row.reminder_message)

        mail.send(to=theList,subject="Don't Forget!",message=row.reminder_message)
    	# FIXME

    	if row.repeat and row.repeat_amount > 0:

            newDate = datetime.datetime.today() + datetime.timedelta(days=row.repeat_offset)
            newRepeatAmount = row.repeat_amount - 1 
            row.update_record(reminder_date  = newDate)
            row.update_record(repeat_amount = newRepeatAmount)

            db.commit()
    time.sleep(50) # check every 50s	

    def checkMail():
       stop1 = "Stop"
       stop2 = "stop"

       m.select(readonly=1)
       (retcode, messages) = m.search(None, '(UNSEEN)')
       if retcode == 'OK':
        #for i in range( latest_email_id, latest_email_id-1, -5 ):
           for i in messages[0].split():
               typ, data = m.fetch( i, '(RFC822)' )
            #m.store(messages[0].replace(' ',','),'+FLAGS','\Seen')
               for response_part in data:
                   if isinstance(response_part, tuple):
                       msg = email.message_from_string(response_part[1])
                       #typ, data = m.store(i,'-FLAGS','\\Seen')
                       varSubject = msg['subject']
                       varFrom = msg['from']
                       ms = str(msg)
                       first = '+'
                       if first in varFrom:
                           if stop1 in ms or stop2 in ms:
                            #mail.send(to=[varFrom],
                            #    subject='Your Reminder',
                            #    message = 'Stopping reminder')
                               typ, data = m.store(i,'+FLAGS','\\Seen')
                               number = str(varFrom)[2:12]
                            #response.flash = number
                       elif varFrom[0:10].isdigit():
                           if stop1 in ms or stop2 in ms:
                            #mail.send(to=[varFrom],
                            #    subject='Your Reminder',
                            #    message = 'Stopping reminder')
                               typ, data = m.store(i,'+FLAGS','\\Seen')
                               number = str(varFrom)[0:10]
                               response.flash = 'success'
