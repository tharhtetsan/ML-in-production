import json
import os
from flask import send_from_directory, request
from flask import Flask, request
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    print(req)

    return {
        'fulfillmentText': 'Hello from the bot world'
    }

# To locally run the app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=3000)
