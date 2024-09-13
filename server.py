from flask import Flask,jsonify,request,session,render_template
import sqlite3
import os 



app=Flask(__name__)

def connect_db():
    db=sqlite3.connect('portfolio_project.db')
    db.execute('CREATE TABLE IF NOT EXISTS Pages (site_id INTEGER PRIMARY KEY, site_name TEXT, site_description TEXT, site_image TEXT)')
    db.close()
connect_db()

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home_page.html')


@app.route('/add_project',methods=['POST'])
def add_project():
    message=None

    try:
        data=request.get_json()
        site_name=data['site_name']
        site_description=data['site_description']
        site_image=data['site_image']
        with sqlite3.connect('portfolio_project.db') as db:
            cursor=db.cursor()
            cursor.execute('INSERT INTO Pages (site_name,site_description,site_image) VALUES (?,?,?)',(site_name,site_description,site_image))
            db.commit()
            message=f'Project {site_name} has been added'
    except Exception as e:
        db.rollback()
        message="Error: "+str(e)
    return jsonify(message=message)
@app.route('/update_project/<int:site_id>',methods=['PUT'])
def update_project(site_id):
    message=None

    try:
        data=request.get_json()
        site_name=data.get('site_name')
        site_description=data.get('site_description')
        site_image=data.get('site_image')
        with sqlite3.connect('portfolio_project.db') as db:
            cursor=db.cursor()
            cursor.execute('''UPDATE Pages SET site_name=?, site_description=?, site_image=? WHERE site_id=?  ''',(site_name,site_description,site_image,site_id))
            db.commit()
            if cursor.rowcount==0:
                return jsonify('Error: Not found '),404
            else:
                message=f'Project {site_name} has been updated'
    except Exception as e:
        db.rollback()
        message='Error: '+str(e)
    return jsonify(message=message)
@app.route('/projects',methods=['GET'])
def projects_page():
    projects_arr=[]
    try:
        with sqlite3.connect('portfolio_project.db') as db:
            db.row_factory=sqlite3.Row 
            cursor=db.cursor()
            cursor.execute('SELECT * FROM Pages')
            projects_arr=cursor.fetchall()
    except Exception as e:
        return jsonify("Error: "+str(e))
    
    for i in projects_arr:
        print(dict(i))
    

    return render_template('projects.html',projects_arr=projects_arr)


@app.route('/contact_info')
def contact_page():
    return render_template('contact_info.html')

if __name__=='__main__':
    app.run(debug=True)