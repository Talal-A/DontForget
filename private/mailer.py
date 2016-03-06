# Attempting to send mail at the correct times.

import time

while True: # inf loop 

    rows = db(db.alarm.user_id==4).select()

    for row in rows:

        mail.send(to=['8059905664@text.att.net'],
             subject='yes?',
             message='hoot')

    time.sleep(30) # check every 30s
                
