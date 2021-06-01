from flaskblog.models import User
from flaskblog import db
from flaskblog import app
from flask import render_template, request, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm,ResetpasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from scripts import Query,filter_prices
from flask_mail import Mail,Message
from random import randint
import threading
import time

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'myasusphone143'
app.config['MAIL_PASSWORD'] = "96I8SLLL"
app.config['MAIL_USE_TLS'] = False

mail = Mail(app)
@app.route("/about")
def about():
    if current_user.is_authenticated:
        return render_template("about.html",title="About")
    return redirect(url_for('login'))
    

logged_users = {}
@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    
    if request.method == "POST" and form.validate():
        # users = User.query.filter_by(email=form.email.data)
        users = User.query.all()
        # print(*users)
        # for user in users:
            # print(user)
        # if(users != None):
        #     flash("User already exists!", "error")
        # else:
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data, confirm_password=form.confirm_password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created for User "+form.username.data +
                " Now you can Login", "success")
        return redirect(url_for('login'))
    return render_template('registration.html', title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # print("login")
    form = LoginForm()
    # print(request.method,form.validate())
    if request.method == "POST":
        
        user = User.query.filter_by(email=form.email.data).first()
        # data = User.query.all()
       
        if user and user.password == form.password.data:
            login_user(user)
         
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful! Please enter valid details","danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/home",methods = ["GET","POST"])

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        print("User auth")
        if(request.method=="POST"):
            item = request.form['search']
            obj = Query()
            # obj.scratch(item)
            start = time.perf_counter()
            t1 = threading.Thread(target=obj.amazon(item))
            t2 = threading.Thread(target=obj.flipkart(item))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            end = time.perf_counter()
            print("operation took",round(end-start,2))

            names,prices,ratings,images,urls = obj.n,obj.p,obj.r,obj.im,obj.u 
            txt = "Other Recommendations".center(100,"-")
            if(names):
                recmd = filter_prices(names,prices,ratings,images,urls,item.lower())
                return render_template("home.html",txt=txt,result="",recmd=recmd,names = names,prices = prices,ratings = ratings, images = images, urls=urls, title="Home",zip = zip)
            else:
                render_template("home.html",title="Home",result="No results Found")
        return render_template("home.html", title="Home")
    return redirect(url_for('login'))

@app.route("/resetpassword",methods = ["GET","POST"])
def resetpassword():
    flag = 0
    form = ResetpasswordForm()
    if request.method == "POST":  
        flag=1
        mail_id = request.form['email']
    # mail.send_message("New message from blog",recipients=["karthikcosmic3@gmail.comn"],
    # body="click on the link provided below")
        user = User.query.filter_by(email=request.form["email"]).first()
        if(user is None):
            flash("User doesnot exists","warning")
            return render_template("resetpassword.html",flag=0,title="Login",form=form)
        msg = Message(
                'Password Reset',
                sender ='myasusphone143@gmail.com',
                recipients = [mail_id]
                )
        otp =''.join(["{}".format(randint(0, 10)) for num in range(0, 6)])
        msg.body = 'use this otp to reset your password\n'+otp
        mail.send(msg)
        otp=otp+"-"+str(user.id)
        flash("Mail sent successfully","success")
        return redirect(url_for('validate',otp=otp))
    return render_template("resetpassword.html",flag=flag,title="Login",form=form)

@app.route("/validate/<otp>",methods = ["GET","POST"])
def validate(otp):   
    form = ResetpasswordForm()
    otp,id=otp.split("-")
    print(form.validate())
    if(request.method=="POST"):
        if(request.form["otp"]==otp):
            user = User.query.filter_by(id=id).first()
            user.password = request.form["password"]
            if(user.password==request.form['confirm_password']):
                db.session.commit()
                flash("Password modified successfully","success")

                return redirect(url_for("login"))
            else:
                flash("Password should match","danger")
        else:
            flash("Invalid otp","danger")
   
    return render_template("resetpassword.html",flag=1,title="Login",form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))