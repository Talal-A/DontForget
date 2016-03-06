from gluon.tools import Mail
from datetime import datetime
import time

mail = Mail()

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'dontforgetyourevent@gmail.com'
mail.settings.login = 'dontforgetyourevent@gmail.com:web2pyucsc'


def user():
    return dict(form=auth())

def index():
    # Display the form and accept input

    form = SQLFORM(db.alarm)

    if form.process().accepted:

        theAddress = ''
        emailnum = form.vars.phone_number

        response.flash = 'Successfully added a reminder!'

        theList = phoneProviderList(emailnum)

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
