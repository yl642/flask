from flask import Flask, jsonify
from datetime import datetime
import requests

app = Flask("time_server")

if __name__ == "__main__":
    # a = {'date': "10/10/1999", 'units': "years"}
    # r = requests.post("http://127.0.0.1:5000/age..", json=a)
    # print(r.text)
    app.run()
