import folium 
from folium import plugins 
import random

def createstart(startloc):
    map = folium.Map(location=startloc, zoom_start=8, tiles='openstreetmap')
    #display map
    folium.Marker(startloc, popup='Start Location',icon=folium.Icon(color='green')).add_to(map)
    map.save('templates/map.html')

def createdest(startloc, destloc):
    map = folium.Map(location=startloc, zoom_start=8, tiles='openstreetmap')
    #display map
    folium.Marker(startloc, popup='Start Location',icon=folium.Icon(color='green')).add_to(map)
    folium.Marker(destloc, popup='Destination Location',icon=folium.Icon(color='red')).add_to(map)
    map.save('templates/map.html')

def plotroute(route1,danger1,route2,danger2,route3,danger3):
    if route1!= None:
        route1 = route1["coordinates"]
        for item in route1:
            temp = item[0]
            item[0]=item[1]
            item[1]=temp
    if route2!= None:
        route2 = route2["coordinates"]
        for item in route2:
            temp = item[0]
            item[0]=item[1]
            item[1]=temp
    
    if route3 != None:
        route3 = route3["coordinates"]
        for item in route3:
            temp = item[0]
            item[0]=item[1]
            item[1]=temp

    if route2 != None:
        map_plot_antroute = folium.Map(location=route2[int((len(route2)/2)-1):int(len(route2)/2)][0], zoom_start=15)
    else:
        map_plot_antroute = folium.Map(location=route1[int((len(route1)/2)-1):int(len(route1)/2)][0], zoom_start=15)

    folium.Marker(route1[0], popup='Start Location',icon=folium.Icon(color='green')).add_to(map_plot_antroute)
    folium.Marker(route1[-1], popup='Destination Location',icon=folium.Icon(color='red')).add_to(map_plot_antroute)
    
    if route1 != None:
        # added lat long to route
        route_lats_longs = route1
        if danger1 in [0,1]:
            color = 'green'
        if danger1 in [2,3]:
            color = 'orange'
        if danger1 in [4,5]:
            color = 'red'
        # Ploting ant-route
        plugins.AntPath(route_lats_longs,color='green').add_to(map_plot_antroute)

    if route2 != None:
        # added lat long to route
        route_lats_longs = route2
        if danger2 in [0,1]:
            color = 'green'
        if danger2 in [2,3]:
            color = 'orange'
        if danger2 in [4,5]:
            color = 'red'
        # Ploting ant-route
        plugins.AntPath(route_lats_longs,color='orange').add_to(map_plot_antroute)

    if route3 != None:
        # added lat long to route
        route_lats_longs = route3
        if danger3 in [0,1]:
            color = 'green'
        if danger3 in [2,3]:
            color = 'orange'
        if danger3 in [4,5]:
            color = 'red'
        # Ploting ant-route
        plugins.AntPath(route_lats_longs,color='red').add_to(map_plot_antroute)

    map_plot_antroute.save('templates/map.html')
