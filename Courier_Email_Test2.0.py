import smtplib
from datetime import date
today = date.today()


    gmail_user = 'nialabtempaturesensor@gmail.com'
    gmail_password = 'NiaLab2003'

    sent_from = gmail_user
    to = ['noah.robit@gmail.com']

    currentInfo = today.strftime("%B %d, %Y") # Current month, date, and year
    subject = currentInfo

    bodyIntro = 'Hello Rohin, the tempature in the room is: '
    body = bodyIntro + str(tempature)

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)


    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")

EmailSender(83.84)
