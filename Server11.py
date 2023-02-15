'''
Author 	        : 	Srikar Uddadi
UTA ID 		    : 	1001962906
Description 	:	The below program will build a connection with Server using a socket and gives command(to print files present in directory-a) to server to process the request.
                    Also, this program will print the synchronized data which is sent back from the Server1.

Citations 	    :   1)https://docs.python.org/3/library/os.path.html
                    2)https://realpython.com/python-sockets/
                    3)https://thispointer.com/python-get-list-of-files-in-directory-with-size/
                    4)https://www.geeksforgeeks.org/python-shutil-copy2-method/
                    5)https://codereview.stackexchange.com/questions/129455/python-program-to-lock-and-unlock-files
'''
import socket
import os
from datetime import *
import time
import shutil
import fcntl
import subprocess

import humanize

#Looping the server to make servers run multiple times
while True:
    #Creating Socket connection
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #Binding the socket connection to 8799 socket
    serverSocket.bind((socket.gethostname(),8799))
    #listening to the connection for 20 times
    serverSocket.listen(100)

    path_split = []
    path_split2 =[]
    list = []
    list2 = []
    list3 = []
    list4 = []
    synclist = []
    synclist2 = []
    synclist3 = []
    final = ""
    res = []
    res2 = []
    a=[]
    count = 0
    li = []
    locked = False

    #Accepting the connection
    clientSocket, clientAddress = serverSocket.accept()

    #Receiving the command arguements from client
    rec_inp = clientSocket.recv(8192)
    rec_inp = rec_inp.decode("utf-8")
    if rec_inp == 'None':
        ind,is_lock = -1, None
    else:
        is_lock,ind = rec_inp.split(" ")
    

    #Getting the contents of the file like name,size and date from the directory files
    for p,d,files in sorted(os.walk("/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a")):
        for i in files:
            if not i.startswith('.') and os.path.isfile(os.path.join(p, i)):
                path2 = os.path.join(p,i)
                path_split.append(path2.split("/"))

    for i in range(len(path_split)):
        path_split2.append(path_split[i][7])
    
    path_split2.sort()
    

    for p,d,files in sorted(os.walk("/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a")):
        for i in files:
            if not i.startswith('.') and os.path.isfile(os.path.join(p, i)):       
                
                path2 =  "/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a/"+path_split2[count]  
                if count == int(ind):
                    if is_lock == "lock":
                        flag = "uchg"
                        subprocess.call(["chflags", flag, path2])
                        locked = True
                        
                    elif is_lock == "unlock":
                        flag = "nouchg"
                        subprocess.call(["chflags", flag, path2])
                        locked = False
                else:
                    locked = False
                    
                
                
                count += 1      
                
                    
                name = os.path.basename(path2)
                    
                size = os.stat(path2)
                    
                size2 = size.st_size
                    
                fTime = time.strftime('%m/%d/%Y', time.localtime(os.path.getmtime(path2)))

                size2 = humanize.naturalsize(size2)
                    
                res.append([name, fTime, size2])

                list.append(name)
                list2.append(fTime)
                list3.append(size2)
                list4.append(locked)

    print("\n")
    print("List of files in directory a")
    print("\n")

    #Concatenating the lists into a single list

    if not list:
        print("No files in directory a")
    else:
        #Printing the files on to the server1 from directory a
        for i in range(len(list)):
            # final += list[i]+'\t'+list2[i]+'\t'+list3[i]+'\n'
            ret = os.access("/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a/"+list[i], os.W_OK)
            if(ret==False):
                print(list[i]+"\t"+list2[i]+"\t"+list3[i]+"\t"+"<locked>")
            else:
                print(list[i]+"\t"+list2[i]+"\t"+list3[i])

    #Creating and Binding socket connections to Server2
    serverSocket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    serverSocket2.connect((socket.gethostname(),3785))

    serverSocket3 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    serverSocket3.connect((socket.gethostname(),8291))

    serverSocket4 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    serverSocket4.connect((socket.gethostname(),9769))

    buffer2 = serverSocket2.recv(8192)

    buffer2 = buffer2.decode('utf-8','strict')

    buffer2 = eval(buffer2)

    buffer3 = serverSocket3.recv(8192)

    buffer3 = buffer3.decode('utf-8')
    # print(buffer3)

    buffer3 = eval(buffer3)

    buffer4 = serverSocket4.recv(8192)

    buffer4 = buffer4.decode('utf-8','strict')

    buffer4 = eval(buffer4)
    #Copying the data to synchronize between directory a and b
    for i in range(len(list)):
            
        if list[i] not in buffer3:
            s = "/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a/"+list[i]
            d = "/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_b"
            shutil.copy2(s,d)
            
    for i in range(len(buffer3)):
        
        if buffer3[i] not in list:
            
            s2 = "/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_b/"+buffer3[i]
            d2 = "/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a"
            shutil.copy2(s2,d2)
               
    for i in range(len(list)):
        for j in range(len(buffer3)):
            if(list[i]==buffer3[j]):
                s1 = str(list2[i])
                s2 = str(buffer4[j])
                m1,d1,y1 = s1.split('/')
                m2,d2,y2 = s2.split('/')
                if(date(int(y1),int(m1),int(d1))>date(int(y2),int(m2),int(d2))):
                    if(os.access("/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a/"+list[i], os.W_OK)==True):
                        s = "/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a/"+list[i]
                        d = "/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_b"
                        shutil.copy2(s,d)
                    
                elif(date(int(y1),int(m1),int(d1))<date(int(y2),int(m2),int(d2))):
                    if(os.access("/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a/"+buffer3[j], os.W_OK)==True):
                        s = "/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_b/"+buffer3[j]
                        d = "/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a"
                        shutil.copy2(s,d)
                    
    print("\n")
    time.sleep(2)
    print("After Synchronization")
    print("\n")
    #Printing the data after synchronization
    for p,d,files in os.walk("/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a"):
        for i in files:
            if not i.startswith('.') and os.path.isfile(os.path.join(p, i)):
                
                path2 = os.path.join(p,i)
                
                name = os.path.basename(path2)
                
                size = os.stat(path2)
                
                size2 = size.st_size
                
                fTime = time.strftime('%m/%d/%Y', time.localtime(os.path.getmtime(path2)))
                
                size2 = humanize.naturalsize(size2)

                res2.append([name, fTime, size2])

                synclist.append(name)
                synclist2.append(fTime)
                synclist3.append(size2)
                

    for i in range(len(synclist)):
        print(synclist[i]+'\t'+synclist2[i]+'\t'+str(synclist3[i]))


    res2.sort(key = lambda res: res[0])

    res2 = str(res2)
    res2 = res2.encode()

    #Sending the data to Client
    clientSocket.send(res2)
    
    # Closing the socket connections
    serverSocket2.close()
    serverSocket3.close()
    serverSocket4.close()

    time.sleep(12)

    clientSocket.close()
    

   

