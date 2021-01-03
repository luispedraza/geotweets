from django.shortcuts import render

from pymongo import MongoClient, DESCENDING as DESC
import json
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Create your views here.

@csrf_exempt
@api_view(['GET'])
def index(request):
    result = []
    if request.method == "GET":
        mongoClient = MongoClient(host="localhost", port=27017)
        geoDB = mongoClient.mydb.geotutorial
        data = geoDB.find().limit(100).sort("timestamp_ms", DESC)
        
        for d in data:
            result.append({
                "id": d["id_str"],
                "msg": d["text"],
                "place": {
                    "lon": d["coordinates"]["coordinates"][0],
                    "lat": d["coordinates"]["coordinates"][1],

                },
                "user_name": d["user"]["name"]
            })
    print("Devolviendo")
    print(result)
    return Response(json.dumps(result))