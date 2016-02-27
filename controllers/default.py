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
            atatt= '@txt.att.net'
            theAddress = emailnum + atatt
        if form.vars.carrier == 'Verizon':
            verizon= '@vtext.com'
            theAddress = emailnum + verizon
        if form.vars.carrier == 'Sprint':
            sprint= '@messaging.sprintpcs.com'
            theAddress = emailnum + sprint
        if form.vars.carrier == 'T-Mobile':
            tmobile= '@tmomail.net'
            theAddress = emailnum + tmobile

        response.flash = 'Successfully added a reminder!'

        if mail.send(to=[theAddress],
                subject='Your reminder',
                message= form.vars.reminder_message
            ):
                response.flash = 'Email sent successfully!'
        else:
                response.flash = 'Failed to send email.'

    return dict(form = form)

def show():
    alarms = db.alarm(request.args[0]) or redirect(URL('index'))

def init():
    return dict(message="Hello")
