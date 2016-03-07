from gluon.tools import Mail
import imaplib
import email
from email.header import decode_header
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
