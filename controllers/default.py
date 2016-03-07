from gluon.tools import Mail
import imaplib
import email
from email.header import decode_header

from datetime import datetime
import time

mail = Mail()

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'dontforgetyourevent@gmail.com'
mail.settings.login = 'dontforgetyourevent@gmail.com:web2pyucsc'

m = imaplib.IMAP4_SSL('imap.gmail.com')
m.login('dontforgetyourevent@gmail.com', 'web2pyucsc')
m.list()
m.select('inbox')

m.select('inbox')
typ, data = m.search(None, 'ALL')
ids = data[0]
id_list = ids.split()

#get the most recent email id
latest_email_id = int( id_list[-1] )

imapdb = DAL("imap://dontforgetyourevent@gmail.com:web2pyucsc@smtp.gmail.com:993", pool_size=1)
imapdb.define_tables()

q = imapdb.INBOX.seen == False
q &= imapdb.INBOX.created == request.now.date()
q &= imapdb.INBOX.size < 6000
unread = imapdb(q).count()

rows = imapdb(q).select()

mymessage = imapdb(imapdb.INBOX.uid == latest_email_id).select().first()

def user():
    return dict(form=auth())

def index():

    form = SQLFORM(db.alarm)
    if form.process().accepted:

        response.flash = 'Successfully added a reminder!'

    return dict(form=form)

def show():
    alarms = db.alarm(request.args[0]) or redirect(URL('index'))

def init():
    return dict(message="Hello")

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

def signedIn():
    form = SQLFORM(db.alarm)
    session.fromSignedIn=1 #flag to indicate coming from signed in to create a new alarm
    return dict(form=form)

def myReminders():
    return dict()

def temp():

    stop1 = "Stop"
    stop2 = "stop"
    help1 = "Help"
    help2 = "help"
    # Display the form and accept input
    #(retcode, messages) = m.search(None, '(UNSEEN)')
    for i in range( latest_email_id, latest_email_id-1, -1 ):
        typ, data = m.fetch( i, '(RFC822)' )
        #if retcode == 'OK':
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                #typ, data = m.store(num,'-FLAGS','\\Seen')
                varSubject = msg['subject']
                varFrom = msg['from']
                ms = str(msg)
                first = '+'
                if first in varFrom:
                    if stop1 in ms or stop2 in ms:
                        mail.send(to=[varFrom],
                            subject='Your Reminder',
                            message = 'Stopping reminder')
                    elif help1 in ms or help2 in ms:
                        mail.send(to=[varFrom],
                            subject='Your Reminder',
                            message = 'Type \'stop\' to prevent reminder messages')
                    else:
                        mail.send(to=[varFrom],
                            subject='Your Reminder',
                            message = 'Invalid response. Please type \'help\' for more options')
