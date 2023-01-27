import email
import sys
from datetime import datetime
from imaplib import IMAP4_SSL
from netrc import netrc
import environ
import imaplib; imaplib.Debug = True
import re

env = environ.Env(
    EMAIL_HOST_USER=str,
    EMAIL_HOST_PASSWORD=str,
    IMAP_GMAIL_SERVER=str,
    SMTP_GMAIL_SERVER=str
)
EMAIL_HOST_USER=env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD=env("EMAIL_HOST_PASSWORD")


 
# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check(email):
 
    # pass the regular expression
    # and the string into the fullmatch() method
    data=re.search(regex, email)
    print("search method",data,type(data))

    if(re.search(regex, email)):

        print("============Valid Email")
 
    else:
        
        print("Invalid Email")


# define since/before dates
# date_format = "%d-%b-%Y" # DD-Mon-YYYY e.g., 3-Mar-2014
# since_date = datetime.strptime(sys.argv[1], date_format)
# before_date = datetime.strptime(sys.argv[2], date_format)

imap_host, imap_port = "imap.gmail.com", 993

login_user = EMAIL_HOST_USER
login_pw = EMAIL_HOST_PASSWORD
# connect to the imap server
mail = IMAP4_SSL(imap_host, imap_port)
mail.login(login_user, login_pw)
try:
    mail.select('inbox')

    # get all messages since since_date and before before_date
    # data = mail.search(None, 'ALL')
    # print(data)
    typ, [msg_ids] = mail.search(None,
        '(since "2-Jan-2023" before "3-Jan-2023")' )

    id_list=msg_ids.split()
    # print((id_list))
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    print("Total number of mail for this week",len(id_list))
    print("FIRST EMAIL ID_COUNT",first_email_id)
    print("LATEST EMAILD ID_COUNT",latest_email_id)
    # get complete email messages in RFC822 format
    # for i in range(latest_email_id,first_email_id, -1): #2831,1,-1
    #     #fetches email using ID
    #     msg_data = mail.fetch(str(i), '(RFC822)' )
    #     for response_part in msg_data:
    #         arr = response_part[0]
    #         if isinstance(arr, tuple):
    #             msg = email.message_from_string(str(arr[1],'utf-8'))
                
    #             email_subject = msg['subject']
    #             email_from = msg['from']
                
    #             print('From : ' ,email_from ,'\n')
    #             print('Subject : ',email_subject , '\n')



    count=1
    for num in id_list:
        typ, msg_data = mail.fetch(num, '(RFC822)')
      
        # print(type(msg_data))
        # print(len(msg_data))
        # print(msg_data[0])
       
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_to = msg['to']
                email_from = msg['from']
                email_date = msg['date']

                
                print("===============start(",count,")==================")
                print('To:',email_to,'\n')
                print('From : ' ,email_from ,'\n')
                print('Subject : ',email_subject , '\n')
                print('date : ' ,email_date ,'\n')
                try:
                    match_data=re.search(regex,email_from)
                    print("after_filtering email : ",match_data.group(0))
                except Exception as e:
                    print(e)
                print("===============end(",count,")==================")
                count+=1
                
finally:
    try:
        mail.close()
    finally:
        mail.logout()