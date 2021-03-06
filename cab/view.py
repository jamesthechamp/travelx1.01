from django.conf import settings
if not settings.configured:
    settings.configure()
import json
import urllib
import simplejson
import googlemaps
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
import requests
from lxml import html
from BeautifulSoup import BeautifulSoup
#from busutil import *
googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'
#def calcuatefare(n):
#    if n<=4:
#        return '100'
#    else:
#        return str(100+(13*(n-4)))
def index(request):
    return render(request,'cabform.html')
def cab(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/')
    src = request.POST.get('from')
    dst = request.POST.get('to')
    startlat,startlong=get_coordinates(str(src),from_sensor=False)
    dstlat,dstlong=get_coordinates(str(dst),from_sensor=False)
#    gdis=googlemaps.Client(key='AIzaSyBcvocj_-OQspLCSu-L6FwNw81ttKbWBxQ')
#    distance=gdis.distance_matrix(src,dst)
#    dis=distance['rows'][0]['elements'][0]['distance']['value']/100
#    price=calcuatefare(dis)
    lat,long=get_coordinates("J.L.N Marg,Malviya Nagar, Jaipur",from_sensor=False)
    lat2,long2=get_coordinates("lnmiit, Jaipur",from_sensor=False)
    url = 'https://api.uber.com/v1/estimates/price'
    parameters = {
        'server_token': 'YcSR2FOOfJMtreWpBeDqeyjDmm8Hj1pSh1ZnQP9h',
        'start_latitude': startlat,
        'start_longitude': startlong,
        'end_latitude': dstlat,
        'end_longitude':dstlong,
    }
    response = requests.get(url, params=parameters)
    data = response.json()
    return render(request,'cab.html',{'data':data['prices']})
def get_coordinates(query, from_sensor=False):
    query = query.encode('utf-8')
    url = 'https://api.uber.com/v1/estimates/price'
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
    else:
        latitude, longitude = None, None
        print query, "<no results>"
    return latitude, longitude
