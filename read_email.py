import smtplib
from email.message import EmailMessage
import traceback 
import imaplib
import email
from bs4 import BeautifulSoup
import json
import requests
import environ

from datetime import datetime,timedelta
import csv  
import re
from dateutil import tz

env = environ.Env(
    EMAIL_HOST_USER=str,
    EMAIL_HOST_PASSWORD=str,
    IMAP_GMAIL_SERVER=str,
    SMTP_GMAIL_SERVER=str,
    EMAIL_HOST_EUROPEA_ID=str,
    EMAIL_HOST_EUROPEA_PASSWORD=str

)
EMAIL_HOST_USER=env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD=env("EMAIL_HOST_PASSWORD")
IMAP_GMAIL_SERVER=env("IMAP_GMAIL_SERVER")
SMTP_GMAIL_SERVER=env("SMTP_GMAIL_SERVER")
EMAIL_HOST_EUROPEA_ID=env("EMAIL_HOST_EUROPEA_ID")
EMAIL_HOST_EUROPEA_PASSWORD=env("EMAIL_HOST_EUROPEA_PASSWORD")

FROM_EMAIL  = EMAIL_HOST_EUROPEA_ID
FROM_PWD    = EMAIL_HOST_EUROPEA_PASSWORD

SMTP_PORT   = 993

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  
exact_email=""
crons_states_list=[]
def date_str_sanitizing(date_str):
    # print("email_date",date_str)
    # print("email_date",type(date_str))

    replacements =[(' ',''),('Mon,',''),('Tue,',''),('Wed,',''),('Thu,',''),('Fri,',''),('Sat,',''),('Sun,','')]
    for char, replacement in replacements:
        if char in date_str:
            date_str = date_str.replace(char, replacement)
    # print("++++++++++++++++++++++++++++++++",date_str[1:17:1])
    # print("++++++++++++++++++++++++++++++++",len(date_str)) 
    return date_str[0:17:1]
def send_mail(msg_content,sub_content):
    print(type(msg_content))
    print((msg_content))
    
    login_user = EMAIL_HOST_USER
    login_pw = EMAIL_HOST_PASSWORD
    sent_from = login_user
    sent_to="vip.wadekar@gmail.com"
    try:

        msg = EmailMessage()
        msg.set_content(msg_content)

        msg['Subject'] = sub_content
        msg['From'] = sent_from
        msg['To'] = sent_to
        # Send the message via our own SMTP server.
        smtp_server = smtplib.SMTP_SSL(SMTP_GMAIL_SERVER, 465)
        smtp_server.login(login_user, login_pw)
        smtp_server.send_message(msg)
        smtp_server.quit()
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print("Error: unable to send email",e)
    except Exception as ex:
        print("Something went wrong….", ex)
def request_url(myobj):
    
    url = 'http://localhost:4000/booking/make_email_entry'
    response = requests.post(url, json = myobj)
    print(response.status_code,response.text)
    # time jsobobj 

    log_content=json.loads(response.text)
    print("log_Content==============",log_content)
    log_file(log_content)
    mail_content=""
    subject_content=""
    
    
    if log_content["error"] == True : 
        mail_content =log_content["message"]+"\nReason: "+log_content["reason"]
        subject_content="Successfully added booking"
    elif log_content["error"] == False:
        mail_content =log_content["message"]
        subject_content="Failed to add booking"
    send_mail(mail_content,subject_content)
def validation_data(date_str):
    replacements =[('=\r\n',''),('th',''),(" ", ""),(',',''),("\t", ""),('Monday',''),('Tuesday',''),('Wednesday',''),('Thursday',''),('Friday',''),('Saturday',''),('Sunday','')]
    for char, replacement in replacements:
        if char in date_str:
            date_str = date_str.replace(char, replacement)
    print(date_str) 
    date_obj = datetime.strptime(date_str, '%d%B%Y')
    date_str=date_obj.strftime("%Y-%m-%d")
    return date_str
def email_subject_sanitizing(email_subject):
    
    print("sanitizing email subject here")
    print(email_subject[19:len(email_subject)])
    property_Name=email_subject[19:email_subject.find("for")]
    print("property_Name : ",property_Name) 
    check_in_out=email_subject[email_subject.find("for")+4:len(email_subject)]
    check_in= check_in_out[:check_in_out.find("-")].replace('\r\n','')
    check_out= check_in_out[check_in_out.find("-")+2:len(check_in_out)].replace('\r\n','')
    print(check_in)
    print(check_out)
    # print("check in",check_in_out[:check_in_out.find("-")])
    # print("check_out",check_in_out[check_in_out.find("-")+2:len(check_in_out)])  
    # obj["guest_name"]=table_tag[6].find("table").find("p").get_text()
    # obj["number_of_guests"]=table_tag[29].find("p").get_text()

    
    
def template_reading(msg_obj,email_from,email_subject):
    main_string = email_subject
    match_string = "Reservation at"
    
   
      
    if email_from == "express@airbnb.com" and (match_string in main_string):
        obj={"channel_name":"Airbnb, Inc"}
        print("=======================start====================")  
        print('From : ' + email_from + '\n')
        print("sub : "+email_subject+'\n')
        email_subject_sanitizing(email_subject)
        
        
    #     obj["property_Name"]=
    # obj["check_in"]
    # obj["check_in"]=validation_data(checkin_str)
    # obj["check_out"]=validation_data(checkout_str)

    """
        if msg_obj.is_multipart():
            for part in msg_obj.walk():
            # <------ iterate over each email part ----->
                content_type = part.get_content_type()
                
                if content_type == 'text/html' :
                    
                    body = part.get_payload()
                    soup = BeautifulSoup(body, "html.parser")
                    body_tag=soup.body
                    table_tag=body_tag.find_all("table")
                    print(len(table_tag))
                    print("==>content<== : ")
                    # print(table_tag[18].find("p").get_text().replace(" guests",""))
                    for i in range (0,len(table_tag)):
                        try:
                            # print("=======================table",i,"====================")
                            # print(table_tag[i].find("p").get_text())
                            
                            # if table_tag[i].get_text().find("guests")>5:
                            if "guests" in table_tag[i].get_text():
                                # print("guests")    
                                print(table_tag[i].get_text())
                            # elif table_tag[i].get_text().find("guest")>4:
                            #     # print("guest")
                            #     print(table_tag[i].find("p").get_text())             
                            # print("=======================table",i,"====================")
                            
                        except Exception as e:
                            print(e)
                        
                        
                    # table_tag = soup.find_all("table")
                    # print(table_tag.prettify())
            """

def date_time_conversion(datetime_str):
    try:
        # METHOD 2: Auto-detect zones:
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        # print("started to convert into date =========",datetime_str)
        utc_mail_datetime_object = datetime.strptime(datetime_str,'%d%b%Y%H:%M:%S') 
        # print("as per UTC Time : ",utc_mail_datetime_object)
        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        utc_mail_datetime_object = utc_mail_datetime_object.replace(tzinfo=from_zone)
        
        # Convert time zone
        central = utc_mail_datetime_object.astimezone(to_zone)
        # print("final datetime : ",central)
        # print("final datetime type : ",type(central),"\n")
        
        # print("dateobj====",utc_mail_datetime_object+timedelta(hours=5,minutes=30),"\n")
        return central
    except Exception as e:
        print(e)

    
def date_time_crone(ist_date_time,email_to,exact_email,email_subject,email_date,org_datetime):
    mail_time=ist_date_time
    # print("\nmail time",(mail_time.time()))

    t1=crons_states_list[0]
    t2=crons_states_list[1]
    
    if mail_time.time()>t1 and mail_time.time()<t2:
        print("=======================================")
        print(mail_time.time())
        print('To:',email_to,'\n')
        print('From : ' ,exact_email ,'\n')
        print('Subject : ',email_subject , '\n')
        print("original_datetime ",org_datetime,'\n')
        print('date : ' ,email_date ,'\n')   


    return True

def log_file(content):
    curr_datetime = datetime.now()
    fieldnames = ["date_time",'log_details']
    try:
        with open('logfile.csv', mode='r') as csv_file:
            with open('logfile.csv', mode='a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)    
                writer.writerow({'date_time':curr_datetime,'log_details':content})
    except FileNotFoundError as error:
        print("============",error)
        with open('logfile.csv', mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'date_time':curr_datetime,'log_details':content})
    except Exception as error:
        print(error)   

def cron_states_csv_writer(t1,time_plus_90_min):
        fieldnames = ["date","time"]
        try:
            with open('cronstates.csv', mode='r') as csv_file:
                with open('cronstates.csv', mode='a') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)    
                    writer.writerow({'date':t1.date(),'time':time_plus_90_min.time()})
        except FileNotFoundError as error:
                # print("============",error)
                with open('cronstates.csv', mode='a') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'date':t1.date(),'time':time_plus_90_min.time()})
        except Exception as error:
            print(error)  

def crons_states():
    
    # start time
    start_time = "12-Jan-2023 12:00:00"
    # end_time = "1:30:00"
    
    t1 = datetime.strptime(start_time, "%d-%b-%Y %H:%M:%S")
    # print("start")
    for i in range(0,12):
        if i==0:
            time_plus_90_min=t1
            crons_states_list.append(time_plus_90_min.time())
            cron_states_csv_writer(t1,time_plus_90_min)
            
                    # print(time_plus_90_min.time())
        

        
        time_plus_90_min=time_plus_90_min+timedelta(hours=2)
        crons_states_list.append(time_plus_90_min.time())
        cron_states_csv_writer(t1,time_plus_90_min)


        
        # print(time_plus_90_min.time())
    # print("end")
    print("cronstates.txt has done")

def airbnb_template_reading(msg_obj,email_from,email_subject):
    main_string = email_subject
    match_string = "Reservation confirmed"
    if email_from == "express@airbnb.com" and (match_string in main_string):
        obj={"channel_name":"Airbnb"}
        print("=======================start====================")  
        print('From : ' + email_from + '\n')
        print("sub : "+email_subject+'\n')
        print("=======================end====================")  

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_GMAIL_SERVER)
        mail.login(EMAIL_HOST_EUROPEA_ID,EMAIL_HOST_EUROPEA_PASSWORD)
        mail.select('inbox')
       
        # data = mail.search(None, 'ALL')
        typ, [msg_ids] = mail.search(None,
        '(since "16-Jan-2023" before "20-Jan-2023")' )
        
        id_list=msg_ids.split()
        
        print("Total number of mail for today",len(id_list))
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        print("FIRST EMAIL ID_COUNT",first_email_id)
        print("LATEST EMAILD ID_COUNT",latest_email_id)

        # my_list=["property_Name","guest_name","number_of_guests","check_in","check_out"]
        count=1
        # for i in range(latest_email_id,latest_email_id-1, -1): #2831,1,-1
            
        for num in id_list:    
            # fetches email using ID  
            typ, msg_data = mail.fetch(num, '(RFC822)')
            for response_part in msg_data:                
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    # print(msg.keys())

                    # print("=============")
                    # for key,value in msg.items():
                    #     print(key,":============>",value)
                        # print(key,":")
                    # print(msg.items()[0])    
                    email_subject =msg['subject']
                    email_to = msg['to']
                    email_from = msg['from']
                    email_date = msg['date']
                    mailed_by=msg['Return-Path']
                    try:
                        match_data=re.search(regex,email_from)
                        exact_email=match_data.group(0)
                        # print("after_filtering email : ",match_data.group(0))
                    except Exception as e:
                        print(e)
                    
                    airbnb_template_reading(msg,exact_email,email_subject)

                    # datetime_str=date_str_sanitizing(email_date)
                    
                    
                    # ist_date_time=date_time_conversion(datetime_str)
                    
                    # date_time_crone(ist_date_time,email_to,exact_email,email_subject,datetime_str,email_date)

                    # print("===============start(",count,")==================")
                    # print('To:',email_to,'\n')
                    # print('From : ' ,exact_email ,'\n')
                    # print('mailed_by : ' ,mailed_by ,'\n')  
                    # print('Subject : ',email_subject , '\n')
                    # print('date : ' ,email_date ,'\n')  
                           
                    # template_reading(msg,exact_email,email_subject)
                    # print("===============end(",count,")==================")
                   

                    # Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
                    # Previous_Date_str=Previous_Date.strftime("%Y-%d-%m %H:%M:%S")
                    # Previous_Date_datetime_obj=datetime.strptime(Previous_Date_str,'%Y-%d-%m %H:%M:%S')                    
                    
                    
                    # now_datetime = datetime.now()
                    # now_plus_30_min = now_datetime - timedelta(minutes = 60)
                    # datetime_str=now_plus_30_min.strftime("%Y-%d-%m %H:%M:%S")
                    # now_plus_30_min_datetime_obj=datetime.strptime(datetime_str,'%Y-%d-%m %H:%M:%S') 
                    # print("time diff+++++++++++++++++++++++++++++++")
                    # print(now_datetime-mail_datetime_object)



                    # if now_datetime >= mail_datetime_object and mail_datetime_object<=now_plus_30_min_datetime_obj:
                    #     print("===============start(",count,")==================")
                    #     print('To:',email_to,'\n')
                    #     print('From : ' ,exact_email ,'\n')
                    #     print('Subject : ',email_subject , '\n')
                    #     print('date : ' ,email_date ,'\n')         
                    #     # template_reading(msg)
                    #     print("===============end(",count,")==================")
                    #     count+=1
                 
                    
                    
                    # datetime_str = '11Jan202310:13:08'
                    # print((datetime_str))
                    

                    # if exact_email == "automated@airbnb.com": 
                  
                      

        #             if email_from == "Infiny Sales <sales@infiny.in>" and email_subject == "Fwd: New Reservation":
        #                 print("=======================start====================")  
                        
        #                 print('From : ' + email_from + '\n')
        #                 print('Subject : ' + email_subject + '\n')
                        

        #                 """
        #                 if msg.is_multipart():
        #                     for part in msg.walk():
        #                     # <------ iterate over each email part ----->
        #                         content_type = part.get_content_type()
                                
        #                         if content_type == 'text/html' :
                                   
        #                             body = part.get_payload()
        #                             soup = BeautifulSoup(body, "html.parser")
                                    
                                    
        #                             table_tag = soup.find_all("table")
        #                             # print(len(table_tag)-5)
        #                             # print((table_tag[6]).find_all('td')[8].find("h4").get_text())
                                    
                                    
        #                             obj={"channel_name":"EUROPEA"}
        #                             start, end = 0, 11
        #                             c=0                                    
        #                             for num in range(start, end + 1):
        #                             # checking condition
        #                                 if num % 2 != 0 and num != 3:
        #                                     # print(num)
        #                                     obj[my_list[c]]=(table_tag[len(table_tag)-5]).find_all('table')[0].find_all("p")[num].get_text().replace('=\r\n','')
        #                                     # print((table_tag[10]).find_all('table')[0].find_all("p")[num].get_text())
        #                                     c+=1
        #                             # for data in (table_tag[10]).find_all('table')[0].find_all("p") :
        #                             #     print(data.get_text())
        #                             json_obj = json.dumps(obj)
        #                             # print(json_obj)
        #                             request_url(obj)
        #                             print("=======================finish====================")    
                         
        #                     """
                  
                    
                         
        #             if email_from == "Infiny Sales <sales@infiny.in>" and email_subject == "Fwd: New reservation from Booking.com":
                        
        #                 print('From : ' + email_from + '\n')
        #                 print('Subject : ' + email_subject + '\n')
        #                 """
        #                 if msg.is_multipart():
        #                     for part in msg.walk():
        #                     # <------ iterate over each email part ----->
        #                         content_type = part.get_content_type()
                                 
        #                         if content_type == 'text/html' :
        #                             body = part.get_payload()
        #                             soup = BeautifulSoup(body, "html.parser")                               
        #                             obj={"channel_name":"Booking.com"}
        #                             # <------ second approach  ------>
        #                             table_tag = soup.find_all("table")
        #                             obj["property_Name"]=table_tag[0].find_all('table')[0].find_all("p")[2].find_all("strong")[0].next_sibling.get_text().replace('=\r\n', '')
        #                             # print(table_tag[0].find_all('table')[0].find_all("p")[2].find_all("strong")[1].get_text().replace('Property ID: ', ''))
                                    
                                   
        #                             guest_data=table_tag[0].find_all('table')[0].find_all("p")[4].find_all("strong")[0].contents[1].replace(": ",'')
        #                             obj["guest_name"]=table_tag[0].find_all('table')[0].find_all("p")[4].find_all("strong")[0].contents[1].replace(": ",'')
        #                             guest_data_len=len(table_tag[0].find_all('table')[0].find_all("p")[4].get_text().split(":"))
                                    
        #                             obj["number_of_guests"]=table_tag[0].find_all('table')[0].find_all("p")[3].find_all("strong")[2].next_sibling
        #                             second_list=["check_in","check_out"]
        #                             # replacements =[('=\r\n',''),('th',''),(" ", ""),("\t", ""),('Monday',''),('Tuesday',''),('Wednesday',''),('Thursday',''),('Friday',''),('Saturday',''),('Sunday','')]
                                   
        #                             for i in range(0,2):
        #                                 date_str=table_tag[0].find_all('table')[0].find_all("p")[3].find_all("strong")[i].next_sibling
        #                                 # for char, replacement in replacements:
        #                                 #     if char in date_str:
        #                                 #         date_str = date_str.replace(char, replacement) 
        #                                 # date_obj = datetime.strptime(date_str, '%d%B%Y')
        #                                 # date_str=date_obj.strftime("%Y-%m-%d")
        #                                 final_date_str=validation_data(date_str)
        #                                 print(final_date_str)
        #                                 obj[second_list[i]]=final_date_str
                                    
        #                             json_obj = json.dumps(obj)
        #                             print(json_obj)
        #                             request_url(obj)
        #                             print("=======================finish====================")  
                                 
        #            """ 
                    
                    
                """    
                    main_string = email_subject
                    match_string = "Reservation confirmed"
                    # if email_from == "Infiny Sales <sales@infiny.in>" and email_subject == "Fwd: Reservation confirmed - Sashini Lokuge arrives 15 Dec":
                    if exact_email == "automated@airbnb.com" and (match_string in main_string):
                        print('From : ' + email_from + '\n')
                        print('Subject : ' + email_subject + '\n')
                       
                        if msg.is_multipart():
                            for part in msg.walk():
                            # <------ iterate over each email part ----->
                                content_type = part.get_content_type()
                                
                                if content_type == 'text/html' :
                                     
                                    body = part.get_payload()
                                    soup = BeautifulSoup(body, "html.parser")
                                    obj={"channel_name":"Airbnb, Inc"}
                                    # <------ second approach  ------>
                                    table_tag = soup.find_all("table")
                                    
                                    # for i in range (5,11):
                                    #     print("=======================table",i,"====================")
                                    #     print(table_tag[i].prettify())        
                                    #     print("=======================table",i,"====================")

                                    # obj["property_Name"]=table_tag[17].find("h2").get_text().replace('=\r\n','')
                                    # obj["guest_name"]=table_tag[6].find("table").find("p").get_text()
                                    # obj["number_of_guests"]=table_tag[29].find("p").get_text()

                                    # checkin_str=table_tag[24].find("p").get_text().replace('=\r\n','').replace('Check-in','').replace('is anytime after 3:00 PM','')
                                    # checkout_str=table_tag[26].find("p").get_text().replace('=\r\n','').replace('Checkout','').replace('by 11:00 AM','')
                                    # obj["check_in"]=validation_data(checkin_str)
                                    # obj["check_out"]=validation_data(checkout_str)
                                    
                                    # json_obj = json.dumps(obj)
                                    
                                    # print(json_obj)
                                    # request_url(obj)
                                    print("=======================finish====================")  
                """
                                
        
    except Exception as e: 
        traceback.print_exc() 
        print(str(e))



# crons_states()
read_email_from_gmail()
# date_time_crone()
