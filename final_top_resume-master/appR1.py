from flask import flash, Flask, render_template, g, Response, url_for, redirect, request
from okta import UsersClient
from flask_oidc import OpenIDConnect
from os import environ
import pandas as pd
from flask import Flask, render_template
from algo import Parse
import sys
import subprocess
import ranking as rk

import pymongo
import base64
from pymongo import MongoClient



app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] =  environ.get("SECRET_KEY")
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
oidc = OpenIDConnect(app)
okta_client = UsersClient("http://dev-363595.okta.com", "006AeB7u4B3zN3IQBYBdXVTluHFvyWucqCqcavGwlt")

verose = False
if "-v" in str(sys.argv):
    verose = True
p = Parse(verose)
data= p.information

@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None

@app.route('/')
def iindex():
    return render_template("index.html")

@app.route("/dashboard")
@oidc.require_login
def dashboard():
    return render_template("dashboard.html")

@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".filter"))


@app.route("/logout")
def logout():
    g.user = None
    oidc.logout()
    return redirect(url_for(".iindex"))

@app.route('/firstpage/')
def firstpage():
    return render_template('firstpage.html')

@app.route('/filter/')
def filter():
    cluster =MongoClient("mongodb+srv://himanshu7:hatekube000@cluster0-umtto.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster.get_database('resume')
    records = db.coll_resume
    count = records.count_documents({})
    return render_template('filter.html', count=count)

@app.route('/newfilterpage/')
def newfilterpage():
    cluster =MongoClient("mongodb+srv://himanshu7:hatekube000@cluster0-umtto.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster.get_database('resume')
    records = db.coll_resume
    count = records.count_documents({})
    return render_template('newfilterpage.html', count=count)

@app.route('/rank/', methods=['GET', 'POST'])
def rank():
    skill_input = list(request.form['skill'].split(","))
    exp_input = request.form['exp']
    print(skill_input)
    print(exp_input)
    # verose = False
    # if "-v" in str(sys.argv):
    #     verose = True
    # p = Parse(verose)
    # data= p.information
    rated_data = rk.filterRanked(data,skill_input,exp_input)
    return render_template('rank.html',data = rated_data)

# --------DATA DOWNLOAD CODE-------
@app.route('/downall/')
def downall():
    # verose = False
    # if "-v" in str(sys.argv):
    #     verose = True
    # p = Parse(verose)
    # data= p.information
    df = pd.DataFrame(data)
    df.to_csv('alldata.csv')
    flash("All data downloaded.")
    # return 'file downloaded\n'
    return render_template('filter.html')



@app.route('/downmail/')
def downmail():
    # verose = False
    # if "-v" in str(sys.argv):
    #     verose = True
    # p = Parse(verose)
    # data= p.information
    df = pd.DataFrame(data)
    df.to_csv('allmail.csv')
    flash("All mails downloaded.")
    return render_template('filter.html')


@app.route('/downcontact/')
def downcontact():
    # verose = False
    # if "-v" in str(sys.argv):
    #     verose = True
    # p = Parse(verose)
    # data= p.information
    df = pd.DataFrame(data)
    df.to_csv('allcontact.csv')
    flash("All phone numbers downloaded.")
    return render_template('filter.html')

#-------------------------------
# def open():
#     chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
#     p = subprocess.Popen([chrome_path, r'file://C:\Users\HimanshuKholiya\Desktop\okta2\Resume\AmanPAnt.pdf']) #This uses 'Subprocess' to open the file
#     returncode = p.wait() 


@app.route('/all/')
def hello():
    # verose = False
    # if "-v" in str(sys.argv):
    #     verose = True
    # p = Parse(verose)
    # data= p.information
    return render_template('home.html', data=data)

@app.route('/allmail/')
def allmail():
    # verose = False
    # if "-v" in str(sys.argv):
    #     verose = True
    # p = Parse(verose)
    # data= p.information
    return render_template('allmail.html', data=data)

@app.route('/allcontact/')
def allcontact():
    # verose = False
    # if "-v" in str(sys.argv):
    #     verose = True
    # p = Parse(verose)
    # data= p.information
    return render_template('allcontact.html', data=data)



if __name__ == '__main__':
    app.run(port=7000,debug=True)