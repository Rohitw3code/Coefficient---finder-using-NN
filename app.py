import numpy as np
from flask import Flask,render_template,request,redirect
app = Flask(__name__)

learning_rate = 0.01
epochs = 10000
bias = 1

no_fields = 2

w = np.random.rand(3) * 10  # create a random weight


def Preceptator(x1, x2, output):
    outputP = w[0] + w[1] * x1 + w[2] * x2

    error0 = learning_rate * (output - outputP) * bias
    error1 = learning_rate * (output - outputP) * x1
    error2 = learning_rate * (output - outputP) * x2

    w[0] += error0
    w[1] += error1
    w[2] += error2

@app.route('/')
def index():
    return render_template("index.html",no_fields = no_fields)


@app.route('/new_field/<int:action_type>')
def increaseField(action_type):
    global no_fields
    if action_type == 1:
        no_fields+=1
    else:
        no_fields-=1
    return render_template("index.html",no_fields = no_fields,f1="No",f2="No")


def getClosestValue(k):
    b = int(k)
    lst = list(range(b - 1, b + 2, 1))  # lst = [b-1,b,b+1]
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - k))]

def Predict(x1, x2):
    value = w[0] + w[1] * x1 + w[2] * x2

    if (value < 0):
        value = int(value)-1
    elif value == 0:
        pass
    else:
        value = int(value)

    final = "y  =  ", getClosestValue(w[0]), " + ", getClosestValue(w[1]), " * x1 + ", getClosestValue(w[2]), " * x2"
    f = ''
    for i in final:
        f += str(i)
    return f,value

@app.route('/',methods = ['POST'])
def trainModel():
    n = 1
    train = []
    while True:
        X1 = request.form.get(f"X1{n}")
        X2 = request.form.get(f"X2{n}")
        Y = request.form.get(f"Y{n}")
        if X1 == None or X2 == None or Y == None:
            break
        if X1.isdigit() or X2.isdigit() or Y.isdigit():
            train.append((int(X1),int(X2),int(Y)))
        n+=1
    for v in train:
        Preceptator(v[0],v[1],v[2])
    X1 = request.form.get("PX1")
    X2 = request.form.get("PX2")
    f = Predict(int(X1),int(X2))

    return render_template("index.html",no_fields = no_fields,f1=f[1],f2=f[0])

# @app.route('/',methods = ['POST'])
# def predictModel():
#     X1 = request.form.get("PX1")
#     X2 = request.form.get("PX2")
#     f = Predict(int(X1),int(X2))
#     return render_template("index.html",no_fields = no_fields,f1=f[0],f2=f[1])


if __name__ == '__main__':
    app.run(debug=True,port=8000)