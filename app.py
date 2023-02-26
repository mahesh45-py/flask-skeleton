from flask import Flask,jsonify, render_template, request
import pandas as pd
from googletrans import Translator


app = Flask(__name__)
translator = Translator()

data = {
    "readable": False,
    "data":[]
}

@app.route('/')
def home():
    print("home page loaded")
    return 'working skeleton inside'

@app.route('/push')
def push():
    return render_template('home.html')

@app.route('/pullView')
def pullView():
    buffer = data
    data = {
        "readable": False,
        "data":[]
    }   
    return render_template("statement.html",data=buffer['data'])

@app.route('/pull')
def pull():
    try:
        if not data['readable']:
            return jsonify({
            'status':False,
            'msg':'Nothing is there bro'
        })
        
        return jsonify({
            'status':True,
            'data':data
        })
        
    except Exception as err:
        return jsonify({
            'status':False,
            'msg':str(err)
        })

@app.route('/pushExel',methods=['GET','POST'])
def pushExel():
    
    
    if request.method == 'POST':
        
        try:
            file = request.files['file']
            df = pd.read_excel(file,header=13)
            for index, row in df.iterrows():
                
                date = str(row[1]).split(' ')[0]
                amount = row[3]
                name = translator.translate(row[10], src='en', dest = 'te').text
                type = row[4]
                if type == 'C':
                    data['readable']=True
                    data["data"].append({
                        'date':date,
                        'name':name,
                        'amount':amount
                    })
                    
            
            return jsonify({
                "status":True,
                "data":data
            })
        except Exception as err:
            print(err)
            return jsonify({
                "status":False,
                "msg":str(err)
            })
    return 'Not gonna work'