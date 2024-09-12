from flask import Flask,jsonify,request,session,render_template
import sqlite3
import os 


app=Flask(__name__)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home_page.html')


@app.route('/projects',methods=['GET'])
def projects_page():
    return render_template('projects.html')


@app.route('/contact_info')
def contact_page():
    return render_template('contact_info.html')

if __name__=='__main__':
    app.run(debug=True)