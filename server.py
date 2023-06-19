import socket
import threading
import sys 
import argparse

#TODO: Implement all code for your server here
# by Kayla Hunt and Justin Effendi

def handle_client(connectionSocket):

	# initialize connected boolean variable
	connected = True

	# things to do while connnected
	while connected:
		message = connectionSocket.recv(1024).decode()

		# handling exit case
		if (message.split(":")[1] == "Exit"):
			exitMessage = message.split(":")[0] + " left the chatroom"
			# send exit message to all clients excluding connection socket
			for client in clientList:
				if client != connectionSocket:
					client.send(exitMessage.encode())
			# print exit message on server
			print(exitMessage)
			sys.stdout.flush()
			clientList.remove(connectionSocket)
			# close connection socket upon exit
			connectionSocket.close()
			connected = False
		else:
			# send a message to all clients excluding connection socket
			for client in clientList:
				if client != connectionSocket:
					client.send(message.encode())
			# print message on server
			print(message)
			sys.stdout.flush()
	pass

# receive listening port number and passcode from the client
parser = argparse.ArgumentParser(description='input listening port number and passcode')
parser.add_argument('-start', action="store_true")
parser.add_argument('-port', type=int, required=True)
parser.add_argument('-passcode', type=str, required=True)
args = parser.parse_args()
serverPortNum = args.port
serverPassCode = args.passcode


# create a server socket and prepare said socket for receiving transmissions
serverPort = serverPortNum
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen()
print('Server started on port ' + str(serverPort) + '. Accepting connections')
sys.stdout.flush()

# list of connection socket - address tuples
clientList = []

while True:
	connectionSocket, addr = serverSocket.accept()

	# receiving passcode from client
	passcode = connectionSocket.recv(1024).decode()

	# check if passcode is valid or not
	if (passcode == serverPassCode):
		passcodeValid = 'true'
		connectionSocket.send(passcodeValid.encode())
		username = connectionSocket.recv(1024).decode()
		joinedMessage = str(username + " joined the chatroom")
		print(joinedMessage)
		sys.stdout.flush()
		for client in clientList:
			client.send(joinedMessage.encode())
		# add connection socket to list
		clientList.append(connectionSocket)
	else:
		passCodeValid = 'false'
		connectionSocket.send(passCodeValid.encode())
		connectionSocket.close()

		# create and start thread
	thread = threading.Thread(target = handle_client, args=(connectionSocket,))
	thread.start()

# Use sys.stdout.flush() after print statemtents

if __name__ == "__main__":
	pass