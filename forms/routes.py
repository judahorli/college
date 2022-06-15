from flask import Flask, render_template, request  #NEW IMPORT -- request
from forms import ContactForm 					# NEW IMPORT LINE
from flask.ext.mail import Message, Mail

mail = Mail()
app = Flask(__name__)    #This is creating a new Flask object

app.secret_key = 'WebDesign'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'dperillo@umich.edu'
app.config["MAIL_PASSWORD"] = 'fortunamajor13!?'
 
mail.init_app(app)
#decorator that links...
@app.route('/')          								#This is the main URL
def default():
    return render_template("index.html", name = "index", title = "HOME")
@app.route('/index')          								#This is the main URL
def home():
    return render_template("index.html", name = "index", title = "HOME")			#The argument should be in templates folder

@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def pageNotFound(e):
    return render_template('500.html'), 500

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    msg = Message(form.subject.data, sender = 'dperillo@umich.edu', recipients=['dperillo@umich.edu', form.email.data])
    msg.body = """
    From: %s <%s>
    %s
    """ % (form.name.data, form.email.data, form.message.data)
    mail.send(msg)

    print "Information posted!"

    form.name.data = ''
    form.email.data = ''
    form.subject.data = ''
    form.message.data = 'Information posted!'

    return render_template('contact.html', form =form)
 
  elif request.method == 'GET':
    return render_template('contact.html', name = "contact", title = "CONTACT", form=form)

if __name__ == '__main__':
    app.run(debug=True)		#debug=True is optional
