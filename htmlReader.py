from bs4 import BeautifulSoup
import re
with open("file1.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")
    print(list(soup.children))
    for item in list(soup.children):
        print(item)
    # p_tag = soup.find_all("p")
    # print(len(p_tag))
    # print(type(p_tag))
    # for par in p_tag:
    #     print("=============================")
       
    #     print(par.get_text())
    #     print("=============================")
    # print(len(soup.find_all("p")))
    # ptag = soup.find_all("p")
    # count=1
    # for data in ptag:
        
    #     print("=================>",((data.contents[0]).text))
    #     print(count)
    #     count+=1
    #     if "2022-11-20" in ((data.contents[0]).text):
    #         print('Given Input',data.contents[0].text)
    
        
# with open("file2.html") as fp:
#     soup = BeautifulSoup(fp, "html.parser")
#     print(len(soup.find_all("p")))
#     tr_tag = soup.find_all("p")
#     print("length of tr_tag",len(tr_tag))
#     for data in tr_tag:
#         # print(".........1111111>>>>>>>>>>>1111111111>",((data.text)))
#         # print(re.findall("2521699",data.text))
#         if 'Property ID:' in data.text:
#             print(' in string',data.text)
#         # else:
#         #     print(' not in string')
        
           
        # for data2 in data:    
        #       a=data2.text.find("Hotel ID")
        #       if not a == -1:    
        #         print(".........1111111>>>>>>>>>>>1111111111>",(data.text))
    

    