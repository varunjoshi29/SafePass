from flask import Flask, render_template
from flask import request
from flask import jsonify

import openrouteservice as ors

from createmap import createstart, createdest, plotroute
from train import starttraining

from statistics import mode

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mayaO'
client = ors.Client(key='5b3ce3597851110001cf624867c31029cd564d6d99171dbb0990af67') # Specify your personal API key
app.config["startGeoobject"] = None
app.config["destGeoobject"] = None

@app.route('/home', methods=['GET'])
def hello():
    app.config["final_dict"], app.config["kmeans"] = starttraining()
    return render_template("main.html")

@app.route('/map')
def plotmap():
    return render_template("map.html")

@app.route('/searchstart', methods=['POST'])
def searchstart():
    data = request.form.get('startname')
    #call api to get start geojson => startgeo
    app.config["startGeoobject"] = getGeoCode(data)
    createstart(app.config["startGeoobject"]["features"][0]["geometry"]["coordinates"])
    return jsonify(status="success", data=app.config["startGeoobject"]["features"][0]["properties"]["label"]) 

@app.route('/searchdest', methods=['POST'])
def searchdest():
    data = request.form.get('destname')
    #call api to get start geojson => destgeo
    app.config["destGeoobject"] = getGeoCode(data)
    createdest(app.config["startGeoobject"]["features"][0]["geometry"]["coordinates"],app.config["destGeoobject"]["features"][0]["geometry"]["coordinates"])
    return jsonify(status="success", data=app.config["destGeoobject"]["features"][0]["properties"]["label"])

def getGeoCode(searchstring):
    # print(dir(client))
    geoobject = client.pelias_search(text=searchstring,size=1)
    return geoobject

@app.route('/getpath', methods=['POST'])
def getpath():
    transport = request.form.get('transport')
    sex = request.form.get('sex')
    descent = request.form.get('descent')
    age = request.form.get('age')
    time = request.form.get('time')

    startcoords = (app.config["startGeoobject"]["features"][0]["geometry"]["coordinates"][0],app.config["startGeoobject"]["features"][0]["geometry"]["coordinates"][1])
    destcoords = (app.config["destGeoobject"]["features"][0]["geometry"]["coordinates"][0],app.config["destGeoobject"]["features"][0]["geometry"]["coordinates"][1])
    path1, path2, path3, routes = calculatepaths(startcoords,destcoords,transport)
    
    danger1 = None
    danger2 = None
    danger3 = None

    if path1 != None:
        danger1 = findpathdangerlevel(path1,sex,descent,age,time)
    
    if path2 != None:
        danger2 = findpathdangerlevel(path2,sex,descent,age,time)
    
    if path3 != None:
        danger3 = findpathdangerlevel(path3,sex,descent,age,time)

    plotroute(path1,danger1,path2,danger2,path3,danger3)
    return {"path1" : path1, "path2" : path2, "path3" : path3, "allroutes" : routes}
    

def findpathdangerlevel(patharray,sex,descent,age,time):
    if sex == 'M':
       M = 1
       F = 0
       X = 0
    elif sex == 'F':
        F = 1
        M = 0
        X = 0
    else :
        X = 1
        F = 0 
        M = 0
    
    A = 0
    B = 0
    H = 0
    O = 0
    W = 0

    if descent == 'A':
        A = 1
    if descent == 'B':
        B = 1
    if descent == 'H':
        H = 1
    if descent == 'O':
        O = 1
    if descent == 'W':
        W = 1

    patharray = patharray["coordinates"]

    i = 0 
    poi = []
    while i < len(patharray):
        pred  = app.config["kmeans"].predict([[time,age,patharray[i][0],patharray[i][1],F,M,X,A,B,H,O,W]])
        poi.append(pred[0])
        i+=4
    
    dangerlevel = mode(poi)
    return dangerlevel 


def calculatepaths(start,dest,transport):
    coords = (start,dest)
    routes  = client.directions(coords,alternative_routes={"share_factor":0.3,"target_count":3,"weight_factor":2},profile=transport)

    decoded1 = None
    decoded2 = None
    decoded3 = None


    if len(routes['routes']) == 1: 
        geometry1 = routes['routes'][0]['geometry']
        decoded1 = ors.convert.decode_polyline(geometry1)
    elif len(routes['routes']) == 2:
        geometry1 = routes['routes'][0]['geometry']
        decoded1 = ors.convert.decode_polyline(geometry1)
        geometry2 = routes['routes'][1]['geometry']
        decoded2 = ors.convert.decode_polyline(geometry2)
    else:
        geometry1 = routes['routes'][0]['geometry']
        decoded1 = ors.convert.decode_polyline(geometry1)
        geometry2 = routes['routes'][1]['geometry']
        decoded2 = ors.convert.decode_polyline(geometry2)
        geometry3 = routes['routes'][2]['geometry']
        decoded3 = ors.convert.decode_polyline(geometry3)

    return decoded1,decoded2,decoded3,routes