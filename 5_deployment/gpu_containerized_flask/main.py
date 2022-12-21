from flask import Flask,url_for, request,render_template
import torch
import os
app = Flask(__name__)

@app.get("/")
def home():
    return " .....  Server is OK ....."


@app.get("/gpu")
def checkVersion():
    gpu_status = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0)
    return "Hello this is {} server :v0.0.2.2 and GPU status : {} : {}".format(os.getenv("_SERVER"),gpu_status,gpu_name)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')