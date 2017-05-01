from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import AccidentData
import json
from .getPaths import getPaths
import sys
import os
import base64 
from ml import predict
import time

@csrf_exempt
def calculateSafePath(request):
	in_data = json.loads(request.body)#request.POST #
	print in_data
	source_coordinates = (in_data['lat1'],in_data['long1'])
	destination_coordinates = (in_data['lat2'],in_data['long2'])
	#print 'Here1'
	routes = getPaths(source_coordinates,destination_coordinates)
	#print 'Here2'


	min_cost = (sys.maxint,sys.maxint)
	min_dist,max_dist = sys.maxint,0
	min_x,min_y,max_x,max_y=sys.maxint,sys.maxint,0,0
	for route in routes:
		bounds = route[3]
		dist = route[1]

		ne = bounds['northeast']
		sw = bounds['southwest']
		# print bounds
		min_x = min([min_x,ne['lat']+0.05,sw['lat']-0.05])
		max_x = max([max_x,ne['lat']+0.05,sw['lat']-0.05])
		min_y = min([min_y,ne['lng']-0.05,sw['lng']+0.05])
		max_y = max([max_x,ne['lng']-0.05,sw['lng']+0.05])


	accident_objs = AccidentData.objects.filter(latitude__range=[min_x,max_x],longitude__range=[min_y,max_y])
	accident_points = []
	for e in accident_objs:
		accident_points.append('%f,%f'%(e.latitude,e.longitude))
	

	acc_data = []

	for j in xrange(len(routes)):
		points = routes[j][2]
		distance = routes[j][1]
		acc_count = 0
		for i in xrange(len(points)-1):
			pt1 = points[i]
			pt2 = points[i+1]
			min_x_here = min(pt1[0],pt2[0])
			max_x_here = max(pt1[0],pt2[0])
			min_y_here = min(pt1[1],pt2[1])
			max_y_here = max(pt1[1],pt2[1])
			for e in accident_objs:
				if  ( min_x_here < e.latitude < max_x_here ) and ( min_x_here < e.longitude < max_y_here ):
					acc_count += e.count
		acc_data.append((acc_count,distance,j))



	try:
		path = min(acc_data)
	except:
		path = (0,0,0)

	print path


	
	ret_data = {
		'accident_points' : accident_points,
		'route_polyline' : routes[path[2]][0],
	}
	print ret_data
	return JsonResponse(ret_data)



@csrf_exempt
def indicateAccident(request):
	in_data = json.loads(request.body)
	print in_data
	lat = round(float(in_data['lat']),4)
	lon = round(float(in_data['long']),4)
	obj,create = AccidentData.objects.get_or_create(latitude=lat,longitude=lon)
	if not create:
		obj.count += 1
	obj.save()
	return JsonResponse({ 'success' : True })



@csrf_exempt
def isBadDriving(request):
	in_data =  request.POST # json.loads(request.body) #
	#print in_data

	image = base64.b64decode(in_data['img'])
	print 'Reached here!'
	filename = str(time.time()).replace('.','-')+'.jpg'
	f = open('safestRoute/ml/input_photos/'+filename,'w').write(image)

	print 'Reached Here!2'
	ans = predict.classify(filename)
	print ans
	os.remove('safestRoute/ml/input_photos/'+filename)
	return JsonResponse({
							'prediction' : ans,
						})
