import RPi.GPIO as GPIO
import time
import board
import neopixel
from picamera import PiCamera
GPIO.setwarnings(False) 

#sets GPIO pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D21
 
# The number of LED lights
num_pixels = 150
 
# The order of the pixel colors - RGB or GRB
ORDER = neopixel.GRB
 
#main neopixel function that calls the light strip with the library
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

#initialize the picamera module and counter 
camera = PiCamera()
imagecounter=0
 
#ultrasonic sensor
#this measures the distance in centimeters by finding distance= time x speed
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    #distance= time x speed
    distance = TimeElapsed * 17150
    distance = round(distance,2)
 
    return distance
 
 #takes photo and names it testImage with the correct counter it is on
def printphoto(imagecounter):
    destinationpicture= ('/home/pi/Documents/testImage')
    #library function that captures images and converts to a jpeg, can be changed to png or another extension
    camera.capture(destinationpicture+str(imagecounter),format='jpeg')
    print("took photo named %s" %destinationpicture+str(imagecounter))
    
 
if __name__ == '__main__':
    try:
        
        
        while True:
            #calls distance function
            dist = distance()
            print ("Measured Distance = %.1f cm" %dist)

            #creates colors that can be choosen from
            red=(255,0,0)
            blue=(0,255,0)
            green= (0,0,255)
            nocolor=(0,0,0)
            #color can be changed by user ex: color=red
            color=green
            
            #camera settings
            camera.start_preview(alpha=150)
            
            if dist < 20:
                #shows color
                pixels.fill(color)
                pixels.show()
                #system pause
                time.sleep(.05)
                #shows no color, "off"
                pixels.fill(nocolor)
                pixels.show()
                #system pause
                time.sleep(.05)   
            elif dist < 40 and dist > 20:
                #shows color
                pixels.fill(color)
                pixels.show()
                #system pause
                time.sleep(.15)
                #shows no color, "off"
                pixels.fill(nocolor)
                pixels.show()
                #system pause
                time.sleep(.15)
            elif dist > 40 and dist < 60:
                #shows color
                pixels.fill(color)
                pixels.show()
                #system pause
                time.sleep(.25)
                #shows no color, "off"
                pixels.fill(nocolor)
                pixels.show()
                #system pause
                time.sleep(.25)
            elif dist > 60 and dist < 80:
                #shows color
                pixels.fill(color)
                pixels.show()
                #system pause
                time.sleep(.35)
                #shows no color, "off"
                pixels.fill(nocolor)
                pixels.show()
                #system pause
                time.sleep(.35)
                #calls the print photo function and then increments the image counter by 1
                printphoto(imagecounter)
                imagecounter+=1
            else:
                #shows no color, "off"
                pixels.fill((0,0,0))
                pixels.show()
                #system pause
                time.sleep(1)
        
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("system stopped by user")
        #shows no color, "off"
        pixels.fill((0,0,0))
        pixels.show()
        #turns off camera preview
        camera.close()
        GPIO.cleanup()
