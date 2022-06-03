# Init
gmail_user = 'nialabtempaturesensor@gmail.com'
gmail_password = 'NiaLab2003'
to = ['noah.robit@gmail.com']

#Function to sent the email
def sendEmail(gmail_user,gmail_password, to, email_text):
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(gmail_user, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")
    
#funtion to make email
def makeEmail(ty):
    today = date.today()
    epoch_time = time.time()
    current_time = time.localtime(epoch_time)

    # Format Current Time and Date
    currentInfo = today.strftime("%b %d")
    if(current_time.tm_min < 10):
        min = '0' + str(current_time.tm_min)
    else:
        min = str(current_time.tm_min)
        
    dateInfo = str(current_time.tm_hour) + ':' + min

    subject = 'Tempature Alarm' +  ' @ ' + dateInfo + ' on ' +  str(today.strftime("%b %d ")) 
    bodyIntro = 'Hello Rohin, the tempature in the room is: '
    body = bodyIntro + str(ty)
    
    #fstring header test
    email_text = 'Subject: {}\n\n{}'.format(subject,body)
    return email_text 
  
#function calls
email_text = makeEmail(ty)
sendEmail(gmail_user,gmail_password, to, email_text)
