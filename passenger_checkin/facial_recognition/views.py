from django.shortcuts import render
from .models import Passenger,flight
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.template import loader
from .recognize import FaceDetect
from .update_status import recognized_id
from django.urls import reverse
# Create your views here.
"""
Need : just a http request 
Has : details about the current flight and passenger count.
Do : Renders the home page of the application
And : start boarding the passenger with a "start boarding" button
And : add  and display the passenger and flight details (just in case you want to add your data and check if it works for you.)

"""
def index(request):
    no_of_passenger = Passenger.objects.count()
    passenger_boarded = Passenger.objects.filter(facedetected=True).count()
    passenger_not_boarded = no_of_passenger - passenger_boarded
    flights = flight.objects.get(flight_no='AI0574')
    
    context = {
        'no_of_passenger':no_of_passenger,
        'passenger_boarded':passenger_boarded,
        'passenger_not_boarded':passenger_not_boarded,
        'flights':flights
    }
    
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context,request))

"""
Need : a http request when you press "start boarding" button
Has : Image frame for rendering image from camera source 
And : "Next" button to go forward with boarding process
Do : Renders a page with image frame where image from camera will be
And : call the methods responsible for recognizing face and  streaming camera frames with respective ticket id
"""
def face(request):
    return render(request,'face.html')

"""
Needs : A camera instance object
Do : calls the get_frame() from Face Detect Class
Yield : Frames which are labelled with ticket_id
Do : Afetr taking 4 frames, destruct the camera insrance object
"""
def gen(camera):
    i = 0
    while i < 4:
        i += 1
        frame = camera.get_frame()
        yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    #destruct camera instance object
    del camera

"""
Takes : a http request to start boarding
Returns : A straming http response to the client side by calling gen() method with a FaceDetect instance object
"""
def facecam_feed(request):
    return StreamingHttpResponse(gen(FaceDetect()),content_type='multipart/x-mixed-replace; boundary=frame')

"""
Needs : a http request by clicking "Next" button on the same web page with image frame stream
If : no face is recognized
Returns : No Face Alert
If : Unknown face is detected
Returns : Unknown Face Alert
Do : get the passenger object with e_ticket_number as on the frame on last page
If : Passenger's face detected who is already boarded
Returns : Already Boarded message and passenger details 
Else : Passenger's face detected who is not already boarded
Returns : Details about the passeneger giving option to confirm boarding
"""
def current_passenger(request):
    
    if len(recognized_id) == 0 or recognized_id[-1] == '0':
        template = loader.get_template('noface.html')
        return HttpResponse(template.render({},request))
    tid = recognized_id[-1]
    if recognized_id[-1] == 'Unknown':
        template = loader.get_template('unknown.html')
        return HttpResponse(template.render({},request))
    
    passenger = Passenger.objects.get(e_ticket_number=tid)
    context = {
        'passenger': passenger,
    }
    if passenger.facedetected == True :
        template = loader.get_template('boarded.html')
        return HttpResponse(template.render(context,request))
    
    template = loader.get_template('current_passenger.html')
    return HttpResponse(template.render(context,request))

"""
Need : A http request by clicking "Generate Boarding Pass" button
Takes : last recognized ticket id
Do : get the passeneger details from database of the passeneger with that particular ticket_id
And : update the status of face_detected
And : get the flight details of the flight the passenger is travelling on.
Returns : Boarding Pass of the current passenger
"""
def generate_boarding_pass(request):
    template = loader.get_template('boardingpass.html')
    tid = recognized_id[-1]
    passenger = Passenger.objects.get(e_ticket_number=tid)
    passenger.facedetected = True
    passenger.save()
    flights = flight.objects.get(flight_no=passenger.flight_no)
    context = {
        'passenger' : passenger,
        'flights' : flights
    }
    return HttpResponse(template.render(context,request))

"""
Needs : A http request on clicking "next passenger" button
Returns : face.html page uing HttpResponseRedirect and reverse
"""
def nextp(request):
    return HttpResponseRedirect(reverse('face'))

"""
Needs : A http request by clicking on "Add Passeneger details" in index page
Returns : Add passenger details form "add1.html"
"""
def add1(request):
    template = loader.get_template('add1.html')
    return HttpResponse(template.render({},request))

"""
Needs : Http request with "submit" button on add passenger details page
Do : takes the input data which were submitted in the passenger details form using POST method
And : save all the details to passenger table (a class in models.py)
Returns : index page using HttpResponseRedirect and reverse
"""
def addpassenger(request):
    f_name = request.POST['first']
    l_name = request.POST['last']
    seat = request.POST['seat']
    etkt = request.POST['etkt']
    pnr = request.POST['pnr']
    Class = request.POST['Class']
    fltno = request.POST['fltno']
    try:
        if Passenger.objects.get(e_ticket_number=etkt) is not None :
            template = loader.get_template('duplicate1.html')
            return HttpResponse(template.render({},request))
    except:
        passenger = Passenger(first_name=f_name,last_name=l_name,seat=seat,e_ticket_number=etkt,pnr=pnr,Class=Class,flight_no=fltno,facedetected=False)
        passenger.save()
        return HttpResponseRedirect(reverse('index')) 

"""
Needs : A http Response with a button click on "Display Passenger Details"
Do : loads the details of all the passengers
Returns : A table with details of passengers
"""
def displaypassenger(request):
    passengers = Passenger.objects.all().values()
    template = loader.get_template('displaypassenger.html')
    context ={
        'passengers' : passengers,
    }
    return HttpResponse(template.render(context,request))

"""
Needs : A http request by clicking on "Add Flight details" in index page
Returns : Add Flight details form "add2.html"
"""
def add2(request):
    template = loader.get_template('add2.html')
    return HttpResponse(template.render({},request))

"""
Needs : Http request with "submit" button on add flight details page
Do : takes the input data which were submitted in the flight detailsform using POST method
And : save all the details to flight table (a class in models.py)
Returns : index page using HttpResponseRedirect and reverse
"""
def addflight(request):
    flight_no = request.POST['flight_no']
    departure_loc = request.POST['departure_loc']
    arrival_loc = request.POST['arrival_loc']
    flight_date = request.POST['flight_date']
    dept_time = request.POST['dept_time']
    arrival_time = request.POST['arrival_time']
    terminal = request.POST['terminal']
    gate = request.POST['gate']
    boarding_time = request.POST['boarding_time']
    try :
        if flight.objects.get(flight_no=flight_no) is not None:
            template = loader.get_template('duplicate2.html')
            return HttpResponse(template.render({},request))
    except:
        Flight = flight(flight_no=flight_no,departure_loc=departure_loc,arrival_loc=arrival_loc,flight_date=flight_date,dept_time=dept_time,arrival_time=arrival_time,terminal=terminal,gate=gate,boarding_time=boarding_time)
        Flight.save()
        return HttpResponseRedirect(reverse('index'))

"""
Needs : A http Response with a button click on "Display Flight Details"
Do : loads the details of all the flights
Returns : A table with details of flights
"""

def displayflight(request):
    flights = flight.objects.all().values()
    template = loader.get_template('displayflight.html')
    context ={
        'flights' : flights,
    }
    return HttpResponse(template.render(context,request))

