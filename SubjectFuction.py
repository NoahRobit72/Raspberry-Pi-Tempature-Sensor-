##
##  This Script makes the subject for the email alarm for the Rasberry Pi Tempature Sensor
##

from datetime import date
import time

def subjectString():
    today = date.today()
    epoch_time = time.time()
    current_time = time.localtime(epoch_time)

    # Format Current Time and Date
    currentInfo = today.strftime("%b %d")
    dateInfo = str(current_time.tm_hour) + ':' + str(current_time.tm_min)

    # Combine all into the subject
    subject = 'Tempature Alarm' +  ' @ ' + dateInfo + ' on ' +  str(today.strftime("%b %d ")) 
    return subject

print(subjectString())

