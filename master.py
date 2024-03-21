import socket
import pickle
import ntplib
from time import ctime
import struct

def send_final_result(result):
    workerip = ['0.0.0.0', '1.1.1.1'] # run with actual ip
    # Send the result to two workers
    print("sending")
    for i in range (voter_num):
        host = workerip[i]
        port = 15467
        server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, port))
        result_list = (result)
        data_to_send = pickle.dumps(result_list)
        server_socket.send(data_to_send)

    # server_socket.close()

def main():
    server_list = [0, 0, 0]
    end_list = [0,0,0]
    id_list = [0] * 100

    # Server configuration
    host = '127.0.0.1' # master private IP
    port = 15469
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))
    while(end_list != [{voter_num*2},{voter_num*2},{voter_num*2}]):
        # Listen for incoming connections
        server_socket.listen()

        print(f"Server listening on {host}:{port}")

        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Receive the list from the client
        data = client_socket.recv(1024)

        received_list = pickle.loads(data)

        # time still good
        if received_list != [1,1,1,-1]:
            # Update the server's list
            if id_list[received_list[len(received_list)-1]] != 1:
                for i in range(len(received_list)-1):
                    server_list[i] += received_list[i]
                
                id_list[received_list[len(received_list)-1]] = 1

                # Print out the updated list
                print(f"Updated list on the server: {server_list}")
        
        # wait till recieve all end messages from clients
        else:
            for i in range(len(received_list)-1):
                end_list[i] += received_list[i]
            print(end_list)
            # if end_list == [{voter_num*2},{voter_num*2},{voter_num*2}]:
            if end_list == [4,4,4]:
                client_socket.close()
                server_socket.close()
                # multicast the final result to all clients
                print(server_list)
                # Close the connection
                print("Receive all ending message from clients.")
                return server_list
                break
                # send final result to clients
    
if __name__ == "__main__":
    voter_num = 2
    server_list = main()
    send_final_result(server_list)