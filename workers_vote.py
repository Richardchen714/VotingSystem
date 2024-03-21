import socket
import pickle
import ntplib
from time import ctime
import datetime
import struct
import ast

end_sent = False
def send_end():
    host = '172.31.18.149' # master private IP
    port = 15469

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    
    # List to send to the server
    client_list = ([1,1,1])

    # Send the list to the server
    data_to_send = pickle.dumps(client_list)
    client_socket.send(data_to_send)

    # Close the connection
    client_socket.close()

def get_ntp_time():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org', version=3)
    return ctime(response.tx_time)

def send_results(votes):
    host = '172.31.18.149' # master private IP
    port = 15469

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    
    # List to send to the server
    client_list = (result)

    # Send the list to the server
    data_to_send = pickle.dumps(client_list)
    client_socket.send(data_to_send)

    # Close the connection
    # client_socket.close()

def main():
    
    # Number of candidates
    num_candidates = 3

    # Initialize vote counts for each candidate
    result = [0] * (num_candidates + 1)

    
    # Get time
    end_time = 'Thu Mar  22 18:06:59 2024'
    end_datetime = datetime.datetime.strptime(end_time, "%a %b %d %H:%M:%S %Y")
    current_time = get_ntp_time()
    current_datetime = datetime.datetime.strptime(current_time, "%a %b %d %H:%M:%S %Y")
        
    if current_datetime<end_datetime:
    # Get votes from each voter
        for i in range(1):
            try:
                id = int(input(f"Please enter your ID: "))
                # Get the candidate number the voter is voting for
                # vote = int(input(f"Voter {i + 1}, enter the candidate number (1 to {num_candidates}): "))
                vote = int(input(f"Please enter the candidate number (1 to {num_candidates}): "))
                current_datetime = datetime.datetime.strptime(get_ntp_time(), "%a %b %d %H:%M:%S %Y")
                if current_datetime>end_datetime:
                    print(f"Now time: {current_time}. Timeover!")
                    result = [1,1,1,-1]
                    return result
                # Validate the candidate number
                if 1 <= vote <= num_candidates:
                    break
                else:
                    print(f"Invalid candidate number. Please enter a number between 1 and {num_candidates}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # Count the vote for the chosen candidate
        result[vote - 1] += 1
        result[num_candidates] = id

        # Display the final vote counts
        print("\nVote counts for each candidate:")
        for i in range(num_candidates):
            print(f"Candidate {i + 1}: {result[i]} votes")
        print(result)
        return result
    else:
        print(f"Now time: {current_time}. Timeover!")
        result = [1,1,1,-1]
        return result
        

def listen_final_result():
    # Listen for incoming connections
    client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(('172.31.19.30', 15467))
    print("connecting...")
    client_socket.listen()
    server_socket, server_address = client_socket.accept()
    print(f"Connection from {server_address}")
    data = server_socket.recv(1024)
    client_socket.close()
    server_socket.close()
    
    # Print the message listened from the master
    print('results from master:', pickle.loads(data))

if __name__ == "__main__":    
    result = main()
    send_results(result)
    send_results(result)
    if result == [1,1,1,-1]:
        listen_final_result()
    