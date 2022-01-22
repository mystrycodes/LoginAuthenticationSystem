from flask import Flask, redirect, request, url_for, session, render_template
from flask_pymongo import PyMongo
import bcrypt


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'login_infodb'
app.config['MONGO_URI'] = 'mongodb://afraz:afraz@cluster0-shard-00-00.zrkia.mongodb.net:27017,cluster0-shard-00-01.zrkia.mongodb.net:27017,cluster0-shard-00-02.zrkia.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-a7707y-shard-0&authSource=admin&retryWrites=true&w=majority'
mongo=PyMongo(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        session['username'] = None
        return redirect('/')
    elif 'username' in session and session['username']: 
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name':request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'),login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return redirect('/')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        users= mongo.db.users
        existing_user = users.find_one({'name':request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'),bcrypt.gensalt())
            users.insert_one({'name':request.form['username'],'password':hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return "User already exist"
    return render_template('register.html')

if __name__=='__main__':
    app.secret_key='secretivekeyagain'
    app.run(debug=True)