from flask import Flask, jsonify
from flask_ngrok import run_with_ngrok
from other_class import OtherClass

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run


@app.route("/", methods=['GET'])
def hello() -> str:
    """
    TODO: _summary_
    """
    return "Hello World"

@app.route("/endpoints/1/") #, methods=[POST])
def my_func():
    bob = ["1","2","3"]
    return jsonify(bob)

if __name__ == '__main__':
    app.run()
