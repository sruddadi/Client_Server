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
import time
import sys
import os

result = []
result2 =[]
#Creating a Socket connection to Server1
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

clientSocket.connect((socket.gethostname(),8799))

#Creating arguements to pass to Server1
if len(sys.argv)<=1:
    msg = 'None'
    clientSocket.send(msg.encode())
else:
    ind = sys.argv[1]+" "+str(sys.argv[2])
    inp2 = ind.encode()
    #sending data to server1
    clientSocket.send(inp2)

#Receiving data from Server1
buffer = clientSocket.recv(8192)
output = buffer.decode('utf-8',"strict")
#Received data from Server1
result =eval(output)

i=0
while i<len(result):
    result2 += result[i]
    i+=1

time.sleep(5)
print()
#Printing the sorted data
print("The data :")
print()
i,j=0,0
#Printing the sorted data to the client terminal
while True:
    if not result2:
        print("No Files in the Servers. Please check again")
    elif(j<len(result2)):
        ret = os.access("/Users/srikaruddadi/Desktop/Distributed_Systems/Lab2/directory_a/"+result2[j], os.W_OK)
        if(ret==False):
            print("["+str(i)+"]"+" "+result2[j]+"\t"+result2[j+1]+"\t"+str(result2[j+2])+"\t"+"<locked>")
        else:
            print("["+str(i)+"]"+" "+result2[j]+"\t"+result2[j+1]+"\t"+str(result2[j+2]))
        j+=3
        i+=1
    else: 
        break

print()
#Closing the socket connection
clientSocket.close()


