import smtplib

def sendEmail(tempature):
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login("nialabtempaturesensor@gmail.com","NiaLab2003")
    server.sendmail("nialabtempaturesensor@gmail.com","noah.robit@gmail.com", str(tempature))
    server.quit()

tempature = input("Enter the Tempature: ")
sendEmail(tempature)

