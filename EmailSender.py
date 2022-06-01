import smtplib

EMAIL_ADDRESS = 'nialabtempaturesensor@gmail.com'
EMAIL_PASSWORD = 'NiaLab2003'

with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

    subject = 'This is a test so see if this works'
    body = 'I hope I dont fail'

    msg = f'Subject: {subject}\n\n{body}'
    msg = 'hello'

    smtp.sendmail(EMAIL_ADDRESS, 'noah.robit@gmail.com', msg)