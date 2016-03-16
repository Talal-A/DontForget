from gluon.tools import Mail
import imaplib
import email
import datetime
from gluon.tools import prettydate

from email.header import decode_header


import time

mail = Mail()

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'dontforgetyourevent@gmail.com'
mail.settings.login = 'dontforgetyourevent@gmail.com:web2pyucsc'

def mailScan():
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


def quick_reminder_birthday():

    form = SQLFORM.factory(
        Field('birthday_name', 'string',  requires = IS_NOT_EMPTY()),
        Field('birthday_date', 'date', requires = IS_DATE()))

    if form.process().accepted:

        user = auth.user_id
        phone = auth.user.phone
        date = form.vars.birthday_date
        time = "09:00:00" # default - remind them at 9am
        message = "Don't forget to wish " + str(form.vars.birthday_name) + " a happy birthday!"
        rep = False

        db.alarm.insert(user_id = user, phone_number = phone, reminder_date = date,
            reminder_time = time, reminder_message = message, repeat = rep)

        redirect(URL('signedIn'))

    else:

        response.flash = form.errors

    return dict(form= form)
#controller for signedIn user
def signedIn():
    #if user not signed in redirect to index/main page
    if not auth.user:
        redirect(URL('default', 'index'))

    form = SQLFORM(db.alarm)
    session.fromSignedIn=1 #flag to indicate coming from signed in to create a new alarm

    #list = myReminders()
    list =  db(db.alarm.phone_number == auth.user.phone).select()

    #list to hold prettydate() times
    remLists = []
    today = datetime.date.today()

    for alarm in list:
        # we only want to display future reminders
        if alarm.reminder_date > today:
            a = prettydate(alarm.reminder_date,T)
            b = alarm.reminder_time
            # place time and prettydate() into obj
            objAB = [a,b]
            #append to list
            remLists.append(objAB)

    return dict(form=form,list=list,remLists=remLists,today=today)

def myReminders():
    list =  db(db.alarm.phone_number == auth.user.phone).select()
    return dict(list=list)

def quickAlarm():
    #using the session object to hold a flag for how display the form
    session.alarmType = "quick"
    form = SQLFORM(db.alarm)
    if form.process().accepted:
        session.alarmType = "none"
        response.flash = 'Alarm Set!!!!!!'
        redirect((URL('signedIn')))
        session.alarmType = "none"
    return dict(form=form)

#controller for the custom form with styling
def display_manual_form():

    form = SQLFORM(db.alarm)

    user1 = db.auth_user
    date = datetime.date
    # if user signed in autofill
    if auth.user:
        phoneNum = auth.user.phone
    # if not leave blank
    else:
        phoneNum = ""

    #responses to form submission
    if form.process(session=None, formname= None, keepvalues=True).accepted:
        if auth.user and not session.fromSignedIn:
            redirect((URL('signedIn')))
        elif auth.user:
            redirect(URL('signedIn'))
        elif not auth.user:
            redirect(URL('reminderSummary'))

        response.flash = 'Successfully added a reminder!'
        redirect(URL('default','signedIn'))

    elif form.errors:
        # TODO FIXME: Remove before pushing live
        response.flash = form.errors
        print "Form Failed"
        # if signed in, will not overwrite users phone number
        if not auth.user:
            phoneNum = form.vars.phone_number #if fail, refill the phone number
    else:
        print "please fill in the form"
        response.flash = 'please fill the form'
    # Note: no form instance is passed to the view
    return dict(form=form,user1=user1,date=date,phoneNum=phoneNum)

def reminderSummary():
    return dict()

def temp():

    stop1 = "Stop"
    stop2 = "stop"

    m.select(readonly=1)
    (retcode, messages) = m.search(None, '(UNSEEN)')
    if retcode == 'OK':
        for i in messages[0].split():
            typ, data = m.fetch( i, '(RFC822)' )
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    varSubject = msg['subject']
                    varFrom = msg['from']
                    ms = str(msg)
                    first = '+'
                    if first in varFrom:
                        if stop1 in ms or stop2 in ms:
                            mail.send(to=[varFrom],
                                subject='Your Reminder',
                                message = 'Stopping all reminders')
                            typ, data = m.store(i,'+FLAGS','\\Seen')
                            number = str(varFrom)[2:12]
                            db.person.insert(name='John')
                    elif varFrom[0:10].isdigit():
                        if stop1 in ms or stop2 in ms:
                            mail.send(to=[varFrom],
                                subject='Your Reminder',
                                message = 'Stopping all reminders')
                            typ, data = m.store(i,'+FLAGS','\\Seen')
                            number = str(varFrom)[0:10]




@auth.requires_login()
def viewall():

    #Row of any friend reqeusts to user
    row = db(db.requests.requestee==auth.user_id).select()
    if row:
        response.flash = 'You have friend requests'
    #First friend request
    x = row.first()
    if x:
        y = x.requester
        response.flash = y
        #Fill the first part of the form in with the logged in user
        db.friends.friend.default=x.requester
    #rowx = db((db.requests.requestee==auth.user_id) & (db.requets.requester==x.requester))
    friendz= SQLFORM(db.friends)
    if friendz.process().accepted:    #### delete the first friend request
        db((db.requests.requestee==auth.user_id) & (db.requests.requester==x.requester)).delete()

    #Lists all the alarms for the user
    list =  db(db.alarm.phone_number == auth.user.phone).select()

    #Form to request friends
    form = SQLFORM(db.requests).process()

    return dict(list=list, form=form, row=row, friendz=friendz)

def addcontact():
    form = SQLFORM(db.addressBook).process()
    return dict(form=form)

def friendsend():
    alarmx = db.alarm(request.args[0]) or redirect(URL('index'))
    #response.flash=alarmx.phone_number
    form = FORM('Enter A Friend`s Name',
              INPUT(_name='number', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.process().accepted:
        check=form.vars.number
        #response.flash=check
        l = db(db.auth_user.id==auth.user_id).select()
        p=l.first()
        #m=db(db.auth_user.id==auth.user_id).select()
        q = db((db.addressBook.user==auth.user_id) & (db.addressBook.contact==check)).select().first()
        if q:
            #response.flash=q.phone_number
            if db.alarm.insert( user_id = auth.user_id, phone_number = q.phone_number, reminder_date = alarmx.reminder_date,
                                reminder_message = alarmx.reminder_message, repeat=False):
                response.flash='email sent'
        #else:
        #    response.flash='not your friend'
    else:
        response.flash='form error'

    return dict(form=form)
