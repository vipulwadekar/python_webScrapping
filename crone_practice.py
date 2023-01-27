# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("Hello world")


from datetime import datetime,timedelta

time_list = ["12:05:00","12:20:00","1:10:00","1:20:00","1:40:00","2:40:00"]
time_format_list=[]
for time in time_list:
    time_format_list.append(datetime.strptime(time, "%H:%M:%S"))

    
# for time_fmt in time_format_list:
#     print(time_fmt.time())


# start time
start_time = "12:00:00"
end_time = "1:30:00"

# convert time string to datetime

t1 = datetime.strptime(start_time, "%H:%M:%S")
print('Start time:', t1.time())

for i in range(0,16):        
    if i==0:
        time_plus_90_min=t1
        print(time_plus_90_min)
        
    time_plus_90_min=time_plus_90_min+timedelta(hours=1,minutes=30)
    print(time_plus_90_min.time())

# t2 = datetime.strptime(end_time, "%H:%M:%S")
# print('End time:', t2.time())

    
# for time_fmt in time_format_list:
#      if time_fmt>t1 or time_fmt<t2:
#          print(time_fmt.time())






# get difference
# delta = t2 - t1
# print("delta diff",(delta))
# print("delta diff",type(delta))









