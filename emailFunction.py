import smtplib

def sendEmail(tempature):
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login("nialabtempaturesensor@gmail.com","NiaLab2003")
    form = "Hello Rohin, the tempature in the room is: "
    msg = form + str(tempature)
    server.sendmail("nialabtempaturesensor@gmail.com","noah.robit@gmail.com",msg)
    server.quit()


tempature = input("Enter the Tempature: ")
sendEmail(tempature)

