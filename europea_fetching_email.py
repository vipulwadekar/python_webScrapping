import imaplib
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from email.message import EmailMessage
import email
import environ
import csv 
import re
import json
from dateutil import tz
import traceback
import requests 
import smtplib
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' 
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


def check_in_out_date_sanitizing(date_str):
    # print("=======does not match==============",date_str) 
    replacements =[(" ", ""),('=\r\n',''),('st',''),('nd',''),('rd',''),('n:',''),('Moay',''),('Suay',''),('Chec',''),('th',''),(',',''),("\t", ""),('Monday',''),('Tuesday',''),('Wednesday',''),('Thursday',''),('Friday',''),('Saturday',''),('Sunday','')]
    try:
    
        for char, replacement in replacements:
            if char in date_str:
                date_str = date_str.replace(char, replacement)
        # print("=====================",date_str)
     
        date_obj = datetime.strptime(date_str, '%d%B%Y')
        date_str=date_obj.strftime("%Y-%m-%d")
       
        return date_str
    except ValueError as e:
        print("Value Error",e)
    except Exception as e:
        print("Exception Error",e)

def property_Name_sanitizing(property_Name_str):
    replacements =[('=\r\ns',''),('B=\r\n',''),('=\r\n','')]
    for char, replacement in replacements:
        if char in property_Name_str:
            property_Name_str = property_Name_str.replace(char, replacement)
    # print("++++++++",property_Name_str)
    return property_Name_str

def guest_name_sanitizing(guest_name_str):
    replacements =[('=\r\n','')]
    for char, replacement in replacements:
        if char in guest_name_str:
            guest_name_str = guest_name_str.replace(char, replacement)
    print("---------------",guest_name_str)
    return guest_name_str
def date_str_sanitizing(date_str):
    # print("email_date",date_str)
    # print("email_date",type(date_str))

    replacements =[(' ',''),('n:',''),('Mon,',''),('Tue,',''),('Wed,',''),('Thu,',''),('Fri,',''),('Sat,',''),('Sun,','')]
    for char, replacement in replacements:
        if char in date_str:
            date_str = date_str.replace(char, replacement)
    # print("++++++++++++++++++++++++++++++++",date_str[0:17:1])
    # print("++++++++++++++++++++++++++++++++",len(date_str)) 
    return date_str[0:17:1]

def ist_datetime_conversion(datetime_str):
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
        # print("utc datetime : ",utc_mail_datetime_object)
        # Convert time zone
        central = utc_mail_datetime_object.astimezone(to_zone)
        # print("final datetime : ",central)
        # print("final datetime type : ",type(central),"\n")
        
        # print("dateobj====",utc_mail_datetime_object+timedelta(hours=5,minutes=30),"\n")
        return central
    except Exception as e:
        print(e)
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
    
    
    if log_content["error"] == False : 
        mail_content =log_content["message"]+"\nReason: "+log_content["reason"]
        subject_content="Successfully added booking"
    elif log_content["error"] == True:
        mail_content =log_content["message"]
        subject_content="Failed to add booking"
    send_mail(mail_content,subject_content)
def rentalunited_template_reading(msg_obj):
     rentalunited_obj={}
     if msg_obj.is_multipart():
            for part in msg_obj.walk():
            # <------ iterate over each email part ----->
                content_type = part.get_content_type()
                
                if content_type == 'text/html' :
                    body = part.get_payload()
                    soup = BeautifulSoup(body, "html.parser")
                    body_tag=soup.body
                    table_tag=body_tag.find_all("table")
                    # print(len(table_tag))
                    # print("==>content<== : ")

                    for data in table_tag[0].find_all('strong'):
                        # print(data.next_sibling.get_text())
                        if data.get_text()=="From Channel:":
                            rentalunited_obj["channel_name"]=data.next_sibling
                            # print(data.next_sibling)
        
                        if data.get_text()=="Guest name":
                            rentalunited_obj["guest_name"]=data.next_sibling.replace('=\r\n','')
                            # print(data.next_sibling)          
                        
                        if data.get_text()=="Property Name:":
                            rentalunited_obj["property_Name"]=property_Name_sanitizing(data.next_sibling)    
                        if data.get_text()=="Checkout:":
                            # print(data.next_sibling)
                            rentalunited_obj["check_out"]=check_in_out_date_sanitizing(data.next_sibling)
                        if data.get_text()=="Number of guests:":
                            rentalunited_obj["number_of_guests"]=(data.next_sibling.replace('<=\r\n/p>',''))
                            # print(data.next_sibling)   

                    

                        try:
                          
                            checkin_data=table_tag[0].find_all('p')[3]
                            checkin_str=checkin_data.get_text()[9:40]
                            
                            rentalunited_obj["check_in"]=check_in_out_date_sanitizing(checkin_str)
                            # j=0
                            # for checkin_data in table_tag[0].find_all('p'):
                            #     j+=1
                            #     if j==4:
                            #         checkin_str=checkin_data.get_text()[9:40]
                            #         rentalunited_obj["check_in"]=check_in_out_date_sanitizing(checkin_str)
 
                        except Exception as e:
                            print(e)
                    json_obj = json.dumps(rentalunited_obj)
                    print("Dict obj : ",(rentalunited_obj))
                    request_url(rentalunited_obj)
                    
def airbnb_template_reading(msg_obj):
    airbnb_obj={}
    if msg_obj.is_multipart():
            for part in msg_obj.walk():
            # <------ iterate over each email part ----->
                content_type = part.get_content_type()
                
                if content_type == 'text/html' :
                    body = part.get_payload()
                    soup = BeautifulSoup(body, "html.parser")
                    body_tag=soup.body
                    table_tag=body_tag.find_all("table")
                    div_tag=body_tag.find_all("div")
                    p_tag=body_tag.find_all("p")

                    i=0
                    for table_tag_data in table_tag:

                        print("==============table_tag_data",(i),"======================")
                        # print(table_tag_data.get_text())
                        # print(table_tag.find("h2").get_text())
                        if (table_tag_data.get_text()) == "Guests":
                            print(div_tag[i+1].get_text())

                        # if "Check in" in table_tag_data.get_text() :
                        #     print(div_tag[i+1].get_text())

                        # if "Check out" in table_tag_data.get_text():
                        #     print(div_tag[i+1].get_text())   
                        print("==============table_tag_data",(i),"======================")
                        i+=1
                    

my_list=["property_Name","guest_name","number_of_guests","check_in","check_out"]


def europea_template_reading(msg_obj):
    
    if msg_obj.is_multipart():
        
        for part in msg_obj.walk():
        # <------ iterate over each email part ----->
           
            content_type = part.get_content_type()
            
            if content_type == 'text/html' :
                
                body = part.get_payload()
                soup = BeautifulSoup(body, "html.parser")
                
                
                table_tag = soup.find_all("table")
                # print(len(table_tag)-5)
                # print((table_tag[6]).find_all('td')[8].find("h4").get_text())
                
                
                obj={"channel_name":"EUROPEA"}
                start, end = 0, 11
                c=0                                    
                for num in range(start, end + 1):
                # checking condition
                    if num % 2 != 0 and num != 3:
                        # print(num)
                        obj[my_list[c]]=(table_tag[len(table_tag)-5]).find_all('table')[0].find_all("p")[num].get_text().replace('=\r\n','')
                        # print((table_tag[10]).find_all('table')[0].find_all("p")[num].get_text())
                        c+=1
                # for data in (table_tag[10]).find_all('table')[0].find_all("p") :
                #     print(data.get_text())
                json_obj = json.dumps(obj)
                # print(json_obj)
                request_url(obj)

def fetching_email_main():
    try:
            mail = imaplib.IMAP4_SSL(IMAP_GMAIL_SERVER)
            mail.login(EMAIL_HOST_EUROPEA_ID,EMAIL_HOST_EUROPEA_PASSWORD)
            mail.select('inbox')
        
            # data = mail.search(None, 'ALL')
            typ, [msg_ids] = mail.search(None,
            '(since "22-Jan-2023" before "24-Jan-2023")' )
            
            id_list=msg_ids.split()
            
            print("Total number of mail for today",len(id_list))
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])
            print("FIRST EMAIL ID_COUNT",first_email_id)
            print("LATEST EMAILD ID_COUNT",latest_email_id)

            for num in id_list:    
                # fetches email using ID  
                typ, msg_data = mail.fetch(num, '(RFC822)')
                for response_part in msg_data:                
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        email_subject =msg['subject']
                        email_to = msg['to']
                        email_from = msg['from']
                        email_date = msg['date']
                        mailed_by=msg['Return-Path']
                        
                        try:
                            match_data=re.search(email_regex,email_from)
                            exact_email=match_data.group(0)
                            # print("after_filtering email : ",match_data.group(0))
        
                        except Exception as e:
                            print("========================",e)
                       
                      
                        try :
                            sanitize_datetime_str=date_str_sanitizing(email_date)
                            ist_converted_datetime_obj=ist_datetime_conversion(sanitize_datetime_str)
                        except Exception as e:
                            print(e)
                        

                        if exact_email =="do-not-reply@rentalsunited.com" and ("New reservation" in email_subject):
                                print("after_filtering email : ",exact_email)
                                print("subject : ",email_subject)
                                print("final datetime : ",ist_converted_datetime_obj)
                                print("final datetime type : ",type(ist_converted_datetime_obj),"\n")
                                rentalunited_template_reading(msg)


                        """
                        current_datetime_object= datetime.now().astimezone(tz.tzlocal())
                        before_90_minute_datetime_obj=(current_datetime_object - timedelta(hours=10)).astimezone(tz.tzlocal())
                       
                        
                        
                        
                        if ist_converted_datetime_obj>=before_90_minute_datetime_obj and ist_converted_datetime_obj<=current_datetime_object:
                            print("coming here")

                            #airbnb template
                            
                            if exact_email =="automated@airbnb.com" and ("Reservation confirmed" in email_subject):
                                 
                                print("after_filtering email : ",exact_email)
                                print("subject : ",email_subject)
                                print("final datetime : ",ist_converted_datetime_obj)
                                print("final datetime type : ",type(ist_converted_datetime_obj),"\n")
                                airbnb_template_reading(msg)

                           
                        
                            #rentalunited template
                            if exact_email =="do-not-reply@rentalsunited.com" and ("New reservation" in email_subject):
                                print("after_filtering email : ",exact_email)
                                print("subject : ",email_subject)
                                print("final datetime : ",ist_converted_datetime_obj)
                                print("final datetime type : ",type(ist_converted_datetime_obj),"\n")
                                rentalunited_template_reading(msg)
                              
                            #europea template
                            
                            if exact_email =="reservation@europea-residences.com" and ("New Reservation" in email_subject) and ("EUROPEA Residences" in email_from) :
                                print("after_filtering email : ",exact_email)
                                print("subject : ",email_subject)
                                print("final datetime : ",ist_converted_datetime_obj)
                                print("final datetime type : ",type(ist_converted_datetime_obj),"\n")
                                europea_template_reading(msg)
                            """

                        
    except Exception as e: 
            traceback.print_exc() 
            print(str(e))

fetching_email_main()