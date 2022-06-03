##
##  This script makes and sends an email.
##

from datetime import date
import time
import smtplib
today = date.today()

# Creates the subject for the email
def subjectString():
    today = date.today()
    epoch_time = time.time()
    current_time = time.localtime(epoch_time)

    # Format Current Time and Date
    currentInfo = today.strftime("%b %d")
    dateInfo = str(current_time.tm_hour) + ':' + str(current_time.tm_min)

    subject = 'Tempature Alarm' +  ' @ ' + dateInfo + ' on ' +  str(today.strftime("%b %d ")) 
    return subject

tempature = input('Enter the Tempature: ')

# Sends the email given a verity of inputs
def sendEmail(gmail_user, gmail_password,sent_from, to, email_text):
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")

# Create the content of the email. Email_text is very fragile and cannot go in a function :(
gmail_user = 'nialabtempaturesensor@gmail.com'
gmail_password = 'NiaLab2003'
sent_from = gmail_user
to = ['noah.robit@gmail.com']
currentInfo = today.strftime("%B %d") # Current month, date, and year
subject = subjectString()
bodyIntro = 'Hello Rohin, the tempature in the room is: '
body = bodyIntro + str(tempature)
email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)


sendEmail = sendEmail('nialabtempaturesensor@gmail.com','NiaLab2003','nialabtempaturesensor@gmail.com','noah.robit@gmail.com',email_text)