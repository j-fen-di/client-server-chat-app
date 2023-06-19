from ast import Str
import socket
import threading
import sys
import argparse
from datetime import datetime
from datetime import timedelta

def chat():
	connection = True
	while connection:
		try:
			message = input("")
			#check if shortcut code
			i = 0
			while i != len(message):
				if message[i] == ":":
					if message[i+1] == ")":
						message = message.replace(":)", "[feeling happy]", 1)
					elif message[i+1] == "(":
						message = message.replace(":(", "[feeling sad]", 1)
					elif message[i:i+7] == ":mytime":
						current_time = datetime.now()
						message = message.replace(':mytime', current_time.strftime('%a %b %d %H:%M:%S %Y'))
					elif message[i:i+5] == ":+1hr":
						current_time =datetime.now()
						new_time = current_time + timedelta(hours = 1)
						message = message.replace(':+1hr', new_time.strftime('%a %b %d %H:%M:%S %Y'))
				i += 1	
			if message == ":Exit":
				connection = False
				message = "" + str(username) + str(message)
			else:
				message = "" + str(username) + ": " + str(message)	
			clientSocket.send(message.encode())
		except EOFError:
			pass
	clientSocket.close()
	

def receive():
	connection = True
	while connection:
		try:
			chat = clientSocket.recv(1024).decode()
			print(chat)
			sys.stdout.flush()
		except:
			clientSocket.close()
			connection = False


#TODO: Implement a client that connects to your server to chat with other clients here

parser = argparse.ArgumentParser()
parser.add_argument('-join', action="store_true")
parser.add_argument('-host', type=str, required=True)
parser.add_argument('-port', type=int, required=True)
parser.add_argument('-username', type=str, required=True)
parser.add_argument('-passcode', type=str, required=True)
args = parser.parse_args()


serverName = args.host
serverPort = args.port
username = args.username
passcode = args.passcode
#create socket connection to server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

#send passcode to server that client entered
clientSocket.send(passcode.encode())

#receive if password is correct or not 
passCorrect = clientSocket.recv(1024).decode()

#if password is correct print connected
if passCorrect == "true":
	clientSocket.send(username.encode())
	print("Connected to " + str(serverName) + " on port " + str(serverPort))
	sys.stdout.flush()

else:
	print("Incorrect passcode")
	sys.stdout.flush()
	clientSocket.close()

receiveThread = threading.Thread(target=receive)
receiveThread.start()

chatThread = threading.Thread(target = chat)
chatThread.start()

if __name__ == "__main__":
	pass