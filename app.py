from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    print("home page loaded")
    return 'working skeleton inside'
