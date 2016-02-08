from gluon.tools import Mail
from gluon.contrib.login_methods.email_auth import email_auth


def user():
    return dict(form=auth())

def index():
    alarms = db().select(db.alarm.ALL, orderby=db.alarm.name)
    form=FORM('Your name:', INPUT(_name='name'), INPUT(_type='redirect'))    
    return dict(alarms=alarms, form=form)



def create():

     form = SQLFORM(db.alarm).process(next=URL('init'))
     form.add_button('Alarms', URL('index'))

     return dict(form=form)

def show():
    alarms = db.alarm(request.args[0]) or redirect(URL('index'))

    mail = Mail()
    ##mail = auth.settings.mailer
    ##mail.settings.tls=True
    mail.settings.server = 'http://smtp.webfaction.com:25'
    mail.settings.sender = 'web2py@cmps183.webfactional.com'
    mail.settings.login = '183mailbox:web2pyucsc'



    att = "@txt.att.net"
    theEmail = alarms.number + att
    if mail:
        x = mail.send(to=['gvelazq3@ucsc.edu'],
            subject='ALARM!',
            message= "YOUR ALARM!AHHHHHHH!LAJDSLJA")
        if x == True:
            response.flash = 'email sent sucessfully.'
        else:
            response.flash = 'fail to send email sorry!'
    else:
        response.flash = 'Unable to send the email'
        
    return dict(alarm=alarms, message=theEmail,form=auth.register())

def init():
    return dict(message="Hello")

