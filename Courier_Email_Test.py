import smtplib
from datetime import date
today = date.today()

## Function to send an email of the tempature. Inputs: sender email, sender email password, destination, tempature
def EmailSender(gmail_user, gmail_password, tempature):
    to = ['noah.robit@gmail.com']
    sent_from = gmail_user
    currentInfo = today.strftime("%B %d, %Y") # Current month, date, and year
    subject = 'Tempature Alarm! ' + currentInfo

    bodyIntro = 'Hello Rohin, the tempature in the room is: '
    body = bodyIntro + str(tempature)

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (gmail_user, ", ".join(to), subject, body)

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")







gmail_user = 'nialabtempaturesensor@gmail.com'
gmail_password = 'NiaLab2003'

EmailSender('nialabtempaturesensor@gmail.com','NiaLab2003',93.7)




