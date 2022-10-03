from flask import Flask,url_for, request,render_template
import torch
import os
app = Flask(__name__)


@app.get("/")
def checkVersion():
    gpu_status = torch.cuda.is_available()
    return "Hello this is {} server :v0.0.2.1 and GPU status : {}".format(os.getenv("_SERVER"),gpu_status)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')