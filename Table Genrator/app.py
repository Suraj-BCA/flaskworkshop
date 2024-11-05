from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

results = []

@app.route('/table',methods=['POST'])
def submit():
    num=int(request.form['num'])
    

    # if submit in request.form:
    for i in range(1, 11):
        result = num * i
        results.append((result)) 

    return render_template('index.html',result=results,num=num , i=i)

    # n = len(results)
    # print(n)

    # for j in n:
    #     a=results[j]


    

if __name__=='__main__':
    app.run(debug=True)