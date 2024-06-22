from functools import partial
import imp
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import Event, Location
from .serializers import EventSerializer, MapMarkerSerializer

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
    {
        'Endpoint': '/events/',
        'method': 'GET',
        'body': None,
        'description': 'Returns an array of events'
    },
      {
        'Endpoint': '/events/id',
        'method': 'GET',
        'body': None,
        'description': 'Returns a single event object'
    },
      {
        'Endpoint': '/events/create/',
        'method': 'POST',
        'body': {},
        'description': 'Creates a new event with data sent in POST request'
    },
    {
        'Endpoint': '/events/id/update/',
        'method': 'PUT',
        'body': {},
        'description': 'Creates an existing event with data sent in POST request'
    },
    {
        'Endpoint': '/events/id/delete',
        'method': 'DELETE',
        'body': None,
        'description': 'Deletes an existing event'
    }
    ]
    return Response(routes)

@api_view(['GET'])
def getMapMarkers(request):
    events = Event.objects.all()
    serializer = MapMarkerSerializer(events, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getEvents(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getEvent(request, pk):
    event = Event.objects.get(id=pk)
    serializer = EventSerializer(event, many = False)
    return Response(serializer.data)

@api_view(['POST'])
def createEvent(request):
    data = request.data
    location_data = data.get('location')

    latitude = location_data.get('latitude')
    longitude = location_data.get('longitude')

    # Create a Location instance
    location = Location.objects.create(latitude=latitude, longitude=longitude, text=location_data.get('text'))

    event = Event.objects.create(
    eventName = data['eventName'],
    markerType = data['markerType'],
    eventDescription = data['eventDescription'],
    location=location,
    team = data['team'],
    
    )

    serializer = EventSerializer(event, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateEvent(request, pk):
    event = Event.objects.get(id=pk)
    serializer = EventSerializer(event, data=request.data, partial=True) # mora da moze i za site da se smene 
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)
    event.delete()
    return Response("The event was deleted")

    