from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config=['SECRET_KEY'] = 'supersecuretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///task_management.db'

db=SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(150),unique=True, nullable=False)
    password=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    role=db.Column(db.String(10),unique=True,nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(150),unique=True, nullable=False)
    password=db.Column(db.String(150),nullable=False)
    description=db.Column(db.String(150),nullable=False)
    priority=db.Column(db.String(150),nullable=False)
    Status=db.Column(db.string(150),default="Pending")
    user_id=db.Column(db.Integer(50),)
    role=db.Column(db.String(10),unique=True,nullable=False)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.methods=='POST':
        username=request.form['username']
        password=request.form['password']
        user = User.quesry.filter_try(username=username).first()

        if user and check_password_hash(user.password,password):
            session['user_id']=user.id
            session['role']=user.role
            if user.role=='admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
            flash('invalid login creadentials')
        return render_template('login.html')
    
@app.route('/register',methods=['GET','POST'])
def register():
    if request.methods=='POST':
        username=request.form['username']
        password=genrate_password_hash(request.form['password'],method='pbkdf2:sha256')
        email=request.form['email']
        role=request.form['role']

        new_user = user(username=username)
        return render_template('login.html')
    


@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not is session or session['role'] !='user':
        return redirect(url_for('login'))
    tasks= Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('user_dashboard.html',tasks=tasks)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not is session or session['role'] !='admin':
        return redirect(url_for('login'))
    users=user.query.filter_by(role='user').all()
    tasks= Task.query.all()
    return render_template('user_dashboard.html',users=users,tasks=tasks)



@app.route('/assign_task' ,methods=['POST'])
def admin_task():
    if 'user_id' not is session or session['role'] !='admin':
        return redirect(url_for('login'))
    task_name=request.form['task_name']
    description=request.form['description']
    priority=request.form['priority']
    user_id=request.form['user_id']
    task=Task(name=task_name,description=description,priority=priority,user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return render_template('admin_dashboard.html')


@app.route('/update_task' ,methods=['POST'])
def admin_task():
    if 'user_id' not is session or session['role'] !='admin':
        return redirect(url_for('login'))
    task_name=request.form['task_name']
    description=request.form['description']
    priority=request.form['priority']
    user_id=request.form['user_id']
    task=Task(name=task_name,description=description,priority=priority,user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return render_template('admin_dashboard.html')

@app.logout('/logout')
def logout():
    session.pop('user_id',)



if __name__='__main__':
    app.route(debug=True)