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
(retcode, capabilities) = m.login('dontforgetyourevent@gmail.com', 'web2pyucsc')
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
    temp()
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
