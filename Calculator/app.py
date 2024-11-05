from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate',methods=['POST'])
def calculate():
    num1=float(request.form['num1'])
    num2=float(request.form['num2'])
    operatation=request.form['operation']

    if operatation=='ADDITION':
        result = num1 + num2

    elif operatation=='SUBTRACTION':
        result = num1 - num2

    elif operatation=='MULTIPLICATION':
        result = num1 * num2

    elif operatation=='DIVISION':
        result = num1 % num2

    return render_template('index.html',result=result,num1=num1,num2=num2,option=operatation)

if __name__=='__main__':
    app.run(debug=True)