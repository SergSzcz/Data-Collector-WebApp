from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy #Alchemy allows you to keep less of code
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'xxx'
db=SQLAlchemy(app)

class Data(db.Model): #createating a class to provide a table in database
    __tablename__="data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(100), unique=True) #email address is not longet that 100 characters and it's uniqe
    height_ = db.Column(db.Integer)
    gender_ = db.Column(db.String)

    def __init__(self, email_, height_, gender_):
        self.email_ = email_
        self.height_ = height_
        self.gender_ = gender_


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST']) #methos is necessary for code to be working with HTML code
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        height = request.form["height_value"]
        gender = request.form["gender_value"]
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data = Data(email,height,gender) #we uses class Data to store our values and then add them to the database
            db.session.add(data)
            db.session.commit()
            av_height = db.session.query(func.avg(Data.height_)).scalar()
            av_height_m = db.session.query(func.avg(Data.height_)).filter(Data.gender_== 'male').scalar()
            av_height_f = db.session.query(func.avg(Data.height_)).filter(Data.gender_== 'female').scalar()
            av_height = round(av_height,1)
            av_height_m = round(av_height_m,1)
            av_height_f = round(av_height_f,1)
            send_email(email,height,av_height,av_height_m,av_height_f,gender)
            print(av_height,av_height_m,av_height_f)
            return render_template("success.html")
        else:
            return render_template("wrong.html")

@app.route("/wrong", methods=['POST']) #methos is necessary for code to be working with HTML code
def wrong():
    if request.method == 'POST':
        return render_template("index.html")

if __name__ == '__main__':
    app.debug=True
    app.run()
