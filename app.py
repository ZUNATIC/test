from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///firstapp.db"
with app.app_context():
    db = SQLAlchemy(app)

#db=SQLALchemy(app)

#making class to define structure of db:

class FirstApp(db.Model):
    sno = db.Column(db.Integer,primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.fname}"
    

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        #check if form fields exist
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        if fname and lname and email:
        #create and commit new record to the database    
            firstapp = FirstApp(fname=fname,lname=lname,email=email)
            db.session.add(firstapp)
            db.session.commit()

    allpeople = FirstApp.query.all()
            #print(allpeople)

    return render_template('index.html',allpeople=allpeople)
    #return "<p>Hello, World!</p>"

@app.route('/delete/<int:sno>')
def delete(sno):
    #first fetching the record with sno
    allpeople = FirstApp.query.filter_by(sno=sno).first()
    #now deleting record
    db.session.delete(allpeople)
    db.session.commit()

    return redirect("/")

@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update(sno):
      if request.method == 'POST':
        #check if form fields exist
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        if fname and lname and email:
        #create and commit new record to the database    
            allpeople = FirstApp.query.filter_by(sno=sno).first()
            allpeople.fname=fname
            allpeople.lname=lname
            db.session.add(allpeople)
            db.session.commit()

      allpeople = FirstApp.query.all()
             #print(allpeople)

      return render_template('index.html',allpeople=allpeople)
    #return "<p>Hello, World!</p>"


@app.route("/Home")
def home():
    return 'Welcome to the Home Page'

if __name__ == "__main__":
    app.run(debug=True)