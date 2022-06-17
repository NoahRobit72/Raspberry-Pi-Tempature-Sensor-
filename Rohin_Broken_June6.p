import os
import csv
import glob
import time, sys
import numpy as np
import matplotlib.pyplot as plt

import smtplib
from datetime import date
import time
import smtplib
today = date.today()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir+'28*')[0]
device_file = device_folder + '/w1_slave'

#fig, ax = plt.subplots()
#myplt, = ax.plot(x,yF,color='k')

def read_temp_raw():
    f = open(device_file,'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3] != 'Y':
        time.sleep(0.2)
        lines = read_temp_raw()
    equal_pos = lines[1].find('t=')
    if equal_pos != -1:
        temp_string = lines[1][equal_pos+2:]
        temp_c = float(temp_string)/1000.0
        return temp_c
    
def open_csv(nowTm,initFlag):
    filename = ('rmTempLOG-DD-%02d.csv'%nowTm.tm_mday)
    if initFlag:
        tag = 'w'
    else:
        tag = 'a'
    csvLogFile = open(filename,tag)
    csvLog = csv.writer(csvLogFile)
    return csvLogFile, csvLog

def init_csv(nowTm,csvLog):
    hdrRow = []
    hdrRow.append(['TODAY:',nowTm.tm_year,nowTm.tm_mon,nowTm.tm_mday])
    hdrRow.append(['HOUR:','MINUTE:','RmTemp-degC:','RmTemp-degF'])
    for hdr in hdrRow:
        csvLog.writerow(hdr)
        
    print("\t".join([str(item) for item in hdrRow[1]]))

def write_temp(nowTm,temp_c,temp_f,csvLog):
    datRow = [nowTm.tm_hour, nowTm.tm_min, temp_c, temp_f]
    printstr = ""
    for item in datRow:
        if item != float:
            printstr = "".join([printstr, str(item),"\t"])
        else:
            printstr = "".join([printstr, "{:.2f}".format(item),"\t"])
    print(printstr)
    csvLog.writerow(datRow)
    
def get_temp(csvLog):
    lines = read_temp_raw()
    temp_c = read_temp()
    temp_f = temp_c*9.0/5.0 + 32.0
    nowTm = time.localtime()
    write_temp(nowTm,temp_c,temp_f,csvLog)
    
    tx = 100*nowTm.tm_hour + nowTm.tm_min
    return tx,temp_f
    
def plot_temp(x,y,axLim):
    nowTm = time.localtime()
    plt.cla()
    plt.plot(x,y,color='k',marker='o',markersize=4)
    plt.axis(axLim)
    plt.ylabel("Temperature in Farheneit")
    plt.xlabel("Time in HH:MM")
    titlestr = ('Romm Temperature Log %04d-%02d-%02d \n Last Update Time HH:MM %04d'%(nowTm.tm_year,nowTm.tm_mon,nowTm.tm_mday,x[-1]))
    plt.title(titlestr)
    savename = ('rmTempPLOT_DD-%02d.png'%nowTm.tm_mday)
    plt.savefig(savename)
    print('>>>>>>>Figure updated>>>>>>>>')

#Set up function. Alt. use os.environ.get and make sure to turn off all security features on the gmail account
def init_email():
    gmail_user = 'nialabtempaturesensor@gmail.com'
    gmail_password = 'NiaLab2003'
#     to = ['noah.robit@gmail.com']
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    return gmail_user, smtp_server
#     return gmail_user,gmail_password,to

    
def make_email(ty):
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

    subject = 'Tempature Alarm!' +  ' @ ' + dateInfo + ' on ' +  str(today.strftime("%b %d ")) 
    bodyIntro = 'Hello Rohin, the tempature in the room is: '
    body = bodyIntro + str(ty)
    
    #fstring header test
    email_text = 'Subject: {}\n\n{}'.format(subject,body)
    return email_text 
    
def send_email(ty,to):
#     gmail_user,gmail_password,to = init_email()
    email_text = make_email(ty)
    gmail_user, smtp_server = init_email();
    
#     smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     smtp_server.ehlo()
#     smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(gmail_user, to, email_text)
    smtp_server.close()
    #print ("Email sent successfully!")
    
def run_init():
    x = [];
    y = [];
    nowTm = time.localtime()
    csvLogFile, csvLog = open_csv(nowTm,True)
    init_csv(nowTm,csvLog)
    return x,y,csvLogFile,csvLog
    
# Define constants
markTa = 20 # --Update figure every fiften mintues
markTb = 2355 # --Reset variables, day is done
tm = 3 # --Interval in minutes between reads
slpTimeA = tm*60 # --Interval between temperature reads tm in seconds, set in ts*60
slpTimeB = 6*60 # --Interval between reset defined to be 6 minutes so that 23:55 becomes 00:01 at least
wtTime = 15 # --Number of minutes to wait before sending email alert again in minutes
txEmail = 0 # --Initialised time at which email was sent

tempUB_F = 82 # Upper bound of temperature in Farheneit
tempLB_F = 81 # Lower bound of temperature in Farheneit         CHANGE BACK to 62

emailTo = ['noah.robit@gmail.com'] ## CHNAGE to rohinb96@gmail.com

# Get init values
x,y,csvLogFile,csvLog = run_init()

try:
    while True: # Main program Loop
        tx,ty = get_temp(csvLog)
        x.append(tx)
        y.append(ty)
        # Check if email needs to be sent
        if ty>tempUB_F or ty<tempLB_F:
            # Check if email has been sent, continue logging if wtTime not lapsed
            dx = tx-txEmail
            if dx >= wtTime:
                print('Temp out of regulation, sending email...')
                send_email(ty,emailTo) 
                txEmail = tx
            else:
                print('>>>>>>>Email sent>>>>>>>>')  #Before
        # Check if it is time to plot and save a figure        
        if time.localtime().tm_min%markTa <=tm:
            plot_temp(x,y,[0, 2400, 60, 100])
            csvLogFile.close()
            csvLogFile, csvLog = open_csv(time.localtime(),False)
            # Check if it is time to reset the system
            if x[-1] > markTb:
                print('Re-initialising plots in 5 minutes')
                csvLogFile.close()
                time.sleep(slpTimeB)
                os.system('clear')
                print('Re-initialising plots...')
                x,y,csvLogFile,csvLog = run_init()
                
        time.sleep(slpTimeA)
        
except KeyboardInterrupt:
    if csvLogFile.closed:
        print('All data saved')
    else:
        csvLogFile.close()
        print('...Now all data is saved')
    sys.exit()

  
