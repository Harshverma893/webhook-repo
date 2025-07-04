from flask import Flask
from flask import json, request

app = Flask(__name__)

my_inf = None

@app.route('/index')
def root_msg():
    global my_inf
    if my_inf == None:
        return "Welcome Guys!"
    else:
        return my_inf

@app.route('/github', methods=['POST'])
def listen_github():
    global my_inf
    if request.headers['Content-Type'] =='application/json':
        my_info = json.dumps(request.json)
        my_inf = my_info
        print(my_info)
        return my_info


if __name__ == "__main__":
    app.run(debug=True)