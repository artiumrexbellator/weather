from flask import Flask,request,render_template,send_file
from Request import Request
import os

app = Flask(__name__)
@app.route('/home')
def index():
    station=request.args.get("station")
    date=request.args.get("date")
    if station != None and date != None:
        try:
            r=Request(station,date)
            data=r.getRawData()["records"]
            r.checkPlot()
            r.checkWordCloud()
            if len(data) > 0:
                return render_template('index.html',station=station,date=date,stations=Request.stations(),records=data)
            else:
                return render_template('404.html',type="data",station="",date="")
        except Exception:
            return render_template('404.html',type="data",station="",date="")
    else:
        return render_template('index.html',station="",date="",stations=Request.stations(),records=[])
@app.route('/download')
def download():
    station=request.args.get("station")
    date=request.args.get("date")
    print(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data'))
    try:
        return send_file(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/')+station+'_'+date+'.json',as_attachment=True)
    except FileNotFoundError:
        return render_template('404.html',type="file",station="",date="")
