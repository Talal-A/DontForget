from gluon.tools import Mail

mail = Mail()

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'dontforgetyourevent@gmail.com'
mail.settings.login = 'dontforgetyourevent@gmail.com:web2pyucsc'


@auth.requires_login()
def hello():
    return dict(auth.user)


def user():
    return dict(form=auth())


def index():
    # Display the form and accept input

    form = SQLFORM(db.alarm)

    if form.process().accepted:
        response.flash = 'Successfully added a reminder!'

    if mail:
        if mail.send(to=['weslylim94@gmail.com'],
                     subject='test',
                     message='test'
                     ):
            print "hello"
            # response.flash = 'email sent sucessfully.'
        else:
            response.flash = 'fail to send email sorry!'
    else:
        response.flash = 'Unable to send the email : email parameters not defined'


        # addition to check if user is logged in

    #if some is logged in return user info
    user = auth.user
    return dict(form=form, name=user)


def show():
    alarms = db.alarm(request.args[0]) or redirect(URL('index'))


def init():
    return dict(message="Hello")
