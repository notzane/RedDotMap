from flask import Flask, request, redirect, url_for, make_response, render_template
import json
import pandas


application = Flask(__name__)

dataDF = pandas.DataFrame(columns=["colors","lat","lon","desc","datetime"])


@application.route('/', methods=['GET', 'POST'])
def form_data():
    global dataDF
    if request.method == 'POST':
        color = request.form['color']
        lat = request.form['lat']
        lon = request.form['lon']
        desc = request.form['desc']
        datetime = request.form['time']

        tmp_dict = {"colors":color,"lat":lat,"lon":lon,"desc":desc,"datetime":datetime}
        tmp_arr = [tmp_dict]
        tempDF = pandas.DataFrame(tmp_arr)
        dataDF = pandas.concat([dataDF, tempDF])
        print(dataDF)

        #write tp scv to save
        info = ",".join([color,lat,lon,desc,datetime])
        with open('events.csv','a') as events:
            events.write(info + "\n")
        #print(info)

    return render_template('index.html')

@application.route('/textpass', methods=['GET', 'POST'])
def text_pass():
    global dataDF
    return render_template('textpass.html', data=dataDF.to_json(orient='split'))

@application.route('/displaypage', methods=['GET', 'POST'])
def display_page():
    global dataDF
    return render_template('DisplayPage.html', data=dataDF.to_json(orient='split'))

if __name__ == '__main__':
    application.run(debug=True)
