from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
a = []
b = []
c = []

@app.route('/taskmanage',methods=['POST'])
def taskmanage():
    task=(request.form['task'])
    user=request.form['user']

    

    if user=='a':
        a.append(task)

    elif user=='b':
        b.append(task)

    elif user=='c':
        c.append(task)


    return render_template('index.html',a=a,b=b,c=c)

if __name__=='__main__':
    app.run(debug=True)