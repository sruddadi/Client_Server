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
import time
import humanize

#Looping the server to make servers run multiple times
while True:
    # Creating Socket connections
    serverSocket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket22 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket3 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Binding the socket connections
    serverSocket2.bind((socket.gethostname(),3785))
    serverSocket22.bind((socket.gethostname(),8291))
    serverSocket3.bind((socket.gethostname(),9769))

    # listening to the connections for 20 times
    serverSocket2.listen(100)
    serverSocket22.listen(100)
    serverSocket3.listen(100)

    sSocket,sAddress = serverSocket2.accept()
    sSocket2,sAddress2 = serverSocket22.accept()
    sSocket3,sAddress3 = serverSocket3.accept()

    list = []
    list2 = []
    list3 = []
    synclist = []
    synclist2 = []
    synclist3 = []
    final = ""
    res = []
    # Getting the contents of the file like name,size and date from the directory files
    for p,d,files in os.walk("/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_b"):
        for i in files:
                
            if not i.startswith('.') and os.path.isfile(os.path.join(p, i)):
                    
                path2 = os.path.join(p,i)
                    
                name = os.path.basename(path2)
                    
                size = os.stat(path2)
                    
                size2 = size.st_size
                    
                fTime = time.strftime('%m/%d/%Y', time.localtime(os.path.getmtime(path2)))
                    
                size2 = humanize.naturalsize(size2)
                    
                res.append([name,fTime,size2])

                list.append(name)
                list2.append(fTime)
                list3.append(size2)

    time.sleep(1)
    print()
    print("List of files in directory b")
    print()

    if not list:
        print("No files in directory b")
    else:
        #printing the files from directory b
        for i in range(len(list)):
            # final += list[i]+'\t'+list2[i]+'\t'+list3[i]+'\n'
            print(list[i]+'\t'+list2[i]+'\t'+str(list3[i]))

    res = str(res)
    res = res.encode()

    res2 = str(list)
    res2 = res2.encode()

    res3 = str(list2)
    res3 = res3.encode()

    sSocket.send(res)
    sSocket2.send(res2)
    sSocket3.send(res3)

    time.sleep(3)
    print()
    print("After Synchronization")
    print()
    #printing the files after synchronization
    for p,d,files in os.walk("/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_b"):
        for i in files:
            if not i.startswith('.') and os.path.isfile(os.path.join(p, i)):
                
                path2 = os.path.join(p,i)
                    
                name = os.path.basename(path2)
                    
                size = os.stat(path2)
                    
                size2 = size.st_size
                    
                fTime = time.strftime('%m/%d/%Y', time.localtime(os.path.getmtime(path2)))
                    
                size2 = humanize.naturalsize(size2)

                synclist.append(name)
                synclist2.append(fTime)
                synclist3.append(size2)
                    

    for i in range(len(synclist)):
        print(synclist[i]+'\t'+synclist2[i]+'\t'+str(synclist3[i]))

    print()

    #closing the socket connections
    sSocket.close()
    sSocket2.close()
    sSocket3.close()