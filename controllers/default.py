from gluon.tools import Mail
mail = Mail()

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'dontforgetyourevent@gmail.com'
mail.settings.login = 'dontforgetyourevent@gmail.com:web2pyucsc'


def user():
    return dict(form=auth())

def index():
    alarms = db().select(db.alarm.ALL, orderby=db.alarm.name)
    form=FORM('Your name:', INPUT(_name='name'), INPUT(_type='redirect'))
    if mail:
        if mail.send(to=['weslylim94@gmail.com'],
                subject='test',
                message= 'test'
            ):
                response.flash = 'email sent sucessfully.'
        else:
                response.flash = 'fail to send email sorry!'
    else:
            response.flash = 'Unable to send the email : email parameters not defined'
    return dict(alarms=alarms, form=form)

def create():

     form = SQLFORM(db.alarm).process(next=URL('init'))
     form.add_button('Alarms', URL('index'))

     return dict(form=form)

def show():
    alarms = db.alarm(request.args[0]) or redirect(URL('index'))

def init():
    return dict(message="Hello")
