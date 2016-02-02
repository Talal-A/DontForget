def user():
    return dict(form=auth())

def index():
    alarms = db().select(db.alarm.ALL, orderby=db.alarm.name)
    form=FORM('Your name:', INPUT(_name='name'), INPUT(_type='redirect'))    
    return dict(alarms=alarms, form=form)



def create():
     """creates a new empty wiki page"""
     form = SQLFORM(db.alarm).process(next=URL('init'))
     form.add_button('Alarms', URL('index'))

     return dict(form=form)

def show():
#  Why images??
#    image = db.image(request.args(0,cast=int)) or redirect(URL('index'))
#    db.post.image_id.default = image.id
#    form = SQLFORM(db.post)
#    if form.process().accepted:
#       response.flash = 'your comment is posted'

 #   comments = db(db.post.image_id==image.id).select()
 #   return dict(image=image, comments=comments, form=form)

    # note no view so just used default created by web2py
    form = db.alarm(request.args(0,cast=int))
    return dict()

def download():
    return response.download(request, db)

def init():

    return dict()