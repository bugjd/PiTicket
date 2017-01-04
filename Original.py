
import requests # Imports the Request Libary 
from time import sleep 

attendee_id = "" # Creating the String Variable for the Attendee Id , it has to be declared before it is used
url = "https://serve.getinvited.to/attendees/put/"
eventid = "4375"
payload = "data=%7B%20%20%20%22data%22%3A%7B%22attendee_id%22%3A"+ attendee_id + "%2C%20%22event_id%22%3A%20"+ eventid +"%7D%2C%22header%22%3A%7B%22applicationId%22%3A%2234333%22%2C%22applicationVersion%22%3A%220.1%22%2C%22deviceId%22%3A%22PiTicket%22%7D%2C%22token%22%3A%22304b943da543cd3f9998664f64b37728eea38012%22%20%7D"
headers = {
    'content-type': "application/x-www-form-urlencoded", # Required for API Connection
    }
 

from SimpleCV import Color,Camera,Display # Starts the Computer Vision Libary 

cam = Camera()  #starts the camera
display = Display() 

while(display.isNotDone()):

 img = cam.getImage() #gets image from the camera

 barcode = img.findBarcode() #finds barcode data from image
 if(barcode is not None): #if there is some data processed
   barcode = barcode[0] 
   result = str(barcode.data)
   attendee_id = result 
   response = requests.request("POST", url, data=payload, headers=headers) # Making Request 
   payload = "data=%7B%20%20%20%22data%22%3A%7B%22attendee_id%22%3A"+ attendee_id + "%2C%20%22event_id%22%3A%20"+ eventid +"%7D%2C%22header%22%3A%7B%22applicationId%22%3A%2234333%22%2C%22applicationVersion%22%3A%220.1%22%2C%22deviceId%22%3A%22PiTicket%22%7D%2C%22token%22%3A%22304b943da543cd3f9998664f64b37728eea38012%22%20%7D"



   if response.text == "{\"status\":200}"  : # Finds the Reponse the Pi got from the request above. 
        print  "Valid Ticket - No " + attendee_id
        sleep(1)
         
   elif response.text == "{\"status\":409,\"error\":{\"heading\":\"Attendee already checked in\",\"message\":\"This ticket has already been checked in\",\"vars\":{\"attendee_id\":"+ attendee_id +",\"event_id\":"+ eventid +"}}}" : 
        print "The system says this ticket has already been checked in - Please ask for assistance - Ticket Number " + attendee_id 
        sleep(1)
       
   elif response.text == "{\"status\":409,\"error\":{\"heading\":\"Invalid Ticket\",\"message\":\"No valid ticket for this event has been found\",\"vars\":{\"attendee_id\":"+ attendee_id +",\"event_id\":"+ eventid +"}}}" :
        print "Ticket not found - Please ask for assistance - QR Code Number " + attendee_id
        sleep(1)
   elif response.text =="{\"status\":401,\"error\":{\"heading\":\"Authentication Failed with Get Invited API\",\"message\":\"Your API token was not accepted.\"},\"data\":null}" :
        attendee_id = "" # Used if There are to many calls to the API at the same time
   else:
        print "Connection Problem - Try again - Please ask for assistance " + (response.text)
        sleep(2)    



   
   barcode = [] #resets the barcode data to empty set

 img.save(display) #shows the image on the screen

 if attendee_id == "": # User Dioagole 
  sleep(0.0001)   
 else:
     print "Please Wait"
     sleep(1)
     attendee_id = ""
     sleep(2)
     print "Ready"
