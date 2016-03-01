from gluon.tools import Mail

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

        if form.vars.carrier == 'ATT':
            atatt = '@txt.att.net'
            theAddress = emailnum + atatt
        if form.vars.carrier == 'Verizon':
            verizon = '@vtext.com'
            theAddress = emailnum + verizon
        if form.vars.carrier == 'Sprint':
            sprint = '@messaging.sprintpcs.com'
            theAddress = emailnum + sprint
        if form.vars.carrier == 'T-Mobile':
            tmobile = '@tmomail.net'
            theAddress = emailnum + tmobile

        response.flash = 'Successfully added a reminder!'

        success = 0
        theList = phoneProviderList(emailnum)
        #for number in theList:
        if mail.send(to=theList,
                subject='Your reminder',
                message=form.vars.reminder_message):
             success += 1
        if success > 0:
            response.flash = 'Email sent successfully!'
        else:
            response.flash = 'Failed to send e-mail'
    return dict(form=form)


def show():
    alarms = db.alarm(request.args[0]) or redirect(URL('index'))



def init():
    return dict(message="Hello")

def phoneProviderList(phonenumber):
    listOfNumbers = []
    #listOfNumbers.append(phonenumber + "@text.wireless.alltel.com") #Alltel
    listOfNumbers.append(phonenumber + "@text.att.net")             #AT&T
    #listOfNumbers.append(phonenumber + "@cingularme.com")           #Cingular
    #listOfNumbers.append(phonenumber + "@mobile.mycingular.com")    #Cingular
    #listOfNumbers.append(phonenumber + "@myboostmobile.com")        #Boost Mobile
    #listOfNumbers.append(phonenumber + "@sms.mycricket.com")        #Cricket
    #listOfNumbers.append(phonenumber + "@mymetropcs.com")           #Metro PCS
    listOfNumbers.append(phonenumber + "@messaging.sprintpcs.com")  #Sprint
    #listOfNumbers.append(phonenumber + "@page.nextel.com")          #Nextel
    #listOfNumbers.append(phonenumber + "@VTEXT.com")                #Straight Talk
    listOfNumbers.append(phonenumber + "@tmomail.net")              #T-Mobile
    #listOfNumbers.append(phonenumber + "@email.uscc.net")           #U.S. Cellular
    listOfNumbers.append(phonenumber + "@vtext.com")                #Verizon
    #listOfNumbers.append(phonenumber + "@vmobl.com")                #Virgin Mobile
    return listOfNumbers
