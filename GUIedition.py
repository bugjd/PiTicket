import requests # Imports the Request Libary 
from time import sleep 
import zbar
attendee_id = "" # Creating the String Variable for the Attendee Id , it has to be declared before it is used
url = "https://serve.getinvited.to/attendees/put/"
eventid = "4375"
payload = "data=%7B%20%20%20%22data%22%3A%7B%22attendee_id%22%3A"+ attendee_id + "%2C%20%22event_id%22%3A%20"+ eventid +"%7D%2C%22header%22%3A%7B%22applicationId%22%3A%2234333%22%2C%22applicationVersion%22%3A%220.1%22%2C%22deviceId%22%3A%22PiTicket%22%7D%2C%22token%22%3A%22304b943da543cd3f9998664f64b37728eea38012%22%20%7D"
headers = {
    'content-type': "application/x-www-form-urlencoded", # Required for API Connection
    }
 

from SimpleCV import * # Starts the Computer Vision Libary 

cam = Camera()  #starts the camera
display = Display() 
img = cam.getImage()
width = img.width
height = img.height
screensize = width * height
divisor = 5 # used for automatically breaking up image.
threshold = 150 # color value to detect blob is a light
validlayer_text = "Welcome Valid Ticket Holder "
Welcomelayer_text = "Welcome to Event Please can QR Code over reader"

# layers - Also known as blobs
def Welcomelayer():
        newlayer = DrawingLayer(img.size())
        points = [(2 * width / divisor, height / divisor),
                                                (3 * width / divisor, height / divisor),
                                                (4 * width / divisor, 2 * height / divisor),
                                                (4 * width / divisor, 3 * height / divisor),
                                                (3 * width / divisor, 4 * height / divisor),
                                                (2 * width / divisor, 4 * height / divisor),
                                                (1 * width / divisor, 3 * height / divisor),
                                                (1 * width / divisor, 2 * height / divisor)
                                        ]
        newlayer.polygon(points, filled=True, color=Color.RED)
        newlayer.setLayerAlpha(75)
        newlayer.text(Welcomelayer_text, (width / 3, height / 2), color=Color.WHITE)

        return newlayer

def INVALIDlayer():
        newlayer = DrawingLayer(img.size())
        points = [(2 * width / divisor, height / divisor),
                                                (3 * width / divisor, height / divisor),
                                                (4 * width / divisor, 2 * height / divisor),
                                                (4 * width / divisor, 3 * height / divisor),
                                                (3 * width / divisor, 4 * height / divisor),
                                                (2 * width / divisor, 4 * height / divisor),
                                                (1 * width / divisor, 3 * height / divisor),
                                                (1 * width / divisor, 2 * height / divisor)
                                        ]
        newlayer.polygon(points, filled=True, color=Color.RED)
        newlayer.setLayerAlpha(75)
        newlayer.text("Try Again or ask for a ticket assistant", (width / 3, height / 2), color=Color.WHITE)

        return newlayer


def validlayer():
        newlayer = DrawingLayer(img.size())
        newlayer.circle((width / 3, height / 3), width / 4, filled=True, color=Color.GREEN)
        newlayer.setLayerAlpha(75)
        newlayer.text(validlayer_text, (width / 2, height / 2), color=Color.WHITE)

        return newlayer


while(display.isNotDone()):

 img = cam.getImage() #gets image from the camera
 min_blob_size = 0.10 * screensize # the minimum blob is at least 10% of screen
 max_blob_size = 0.80 * screensize # the maximum blob is at most 80% of screen
 blobs = img.findBlobs(minsize=min_blob_size, maxsize=max_blob_size) # get the largest blob on the screen

 if attendee_id == "": 
   layer = Welcomelayer()
   

 barcode = img.findBarcode() #finds barcode data from image
 if(barcode is not None): #if there is some data processed
   barcode = barcode[0] 
   result = str(barcode.data)
   attendee_id = result 
   response = requests.request("POST", url, data=payload, headers=headers) # Making Request 
   payload = "data=%7B%20%20%20%22data%22%3A%7B%22attendee_id%22%3A"+ attendee_id + "%2C%20%22event_id%22%3A%20"+ eventid +"%7D%2C%22header%22%3A%7B%22applicationId%22%3A%2234333%22%2C%22applicationVersion%22%3A%220.1%22%2C%22deviceId%22%3A%22PiTicket%22%7D%2C%22token%22%3A%22304b943da543cd3f9998664f64b37728eea38012%22%20%7D"



   if response.text == "{\"status\":200}"  : # Finds the Reponse the Pi got from the request above. 
        print  "Valid Ticket - No " + attendee_id
        layer = validlayer()
        sleep(4)
         
   elif response.text == "{\"status\":409,\"error\":{\"heading\":\"Attendee already checked in\",\"message\":\"This ticket has already been checked in\",\"vars\":{\"attendee_id\":"+ attendee_id +",\"event_id\":"+ eventid +"}}}" : 
        print "The system says this ticket has already been checked in - Please ask for assistance - Ticket Number " + attendee_id 
        layer = INVALIDlayer()
       
   elif response.text == "{\"status\":409,\"error\":{\"heading\":\"Invalid Ticket\",\"message\":\"No valid ticket for this event has been found\",\"vars\":{\"attendee_id\":"+ attendee_id +",\"event_id\":"+ eventid +"}}}" :
        print "Ticket not found - Please ask for assistance - QR Code Number " + attendee_id
       
   elif response.text =="{\"status\":401,\"error\":{\"heading\":\"Authentication Failed with Get Invited API\",\"message\":\"Your API token was not accepted.\"},\"data\":null}" :
        attendee_id = "" # Used if There are to many calls to the API at the same time
   else:
        print "Connection Problem - Try again - Please ask for assistance " + (response.text)
        Welcomelayer_text = "Try Again then - Please ask for help "
        
   
   barcode = [] #resets the barcode data to empty set

 img.addDrawingLayer(layer) 
 img.save(display) #shows the image on the screen

 if attendee_id == "": # User Dioagole 
  sleep(0.0001)
  
 else:
     sleep(1)
     



