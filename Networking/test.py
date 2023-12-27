import socket
import struct
import time

import socket
import struct
import time

def serialise_player(player):
    return struct.pack('=HBHHhBhh', *player)

def deserialise_request(request_data):
    # Keep the logic consistent with the go, to break down a request we should always go through a two step process.
    player_data = request_data[5:]  # Skip the first 5 bytes
    return deserialise_player(player_data)

def deserialise_player(data):
    # MAJOR ALERT ----- Go does not pad values but python does so you have to add the equals sign otherwise you get very very fucky wireshark answers.
    # struct format for player data: H = uint16, B = uint8, HH = two uint16, h = int16, B = uint8, hh = two int16
    format_string = '=HBHHhBhh'
    unpacked_data = struct.unpack(format_string, data)
    return unpacked_data

def send_request( request_type, player):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            # Serialize the player data
            player_data = serialise_player(player)

            # Payload length (int32)
            # We have to put this in on the python side as we need it for serialisation on go-side
            # Holy shit this was a pain in the ass, spent ages on wireshark figuring out that
            # 4 bytes were missing and what they were
            # Was the payload length 

            # It's to do with the way binarisation works in go, you have to define a fixed size because binarisation does not like unknown sized onjects
            # for generalisation i had to make the payload an undefined size in go, but i have to keep a standard.
            payload_length = len(player_data)
             
            # 'B' for request type (uint8) and 'I' for payload length (int32)
            
            request_data = struct.pack('=BI', request_type, payload_length) + player_data
            # Python requires you put it in yourself and go automatically does it.

            # Send the request
            sock.sendto(request_data, (host, port))
            
            start_time = time.time()
            
            # Useful for debugging purposes
            # local_ip, local_port = sock.getsockname()
            # print(f"Local IP: {local_ip}, Local Port: {local_port}")
            sock.settimeout(5)  # Timeout in seconds
            
            # Attempt to receive the response
            try:
                response = sock.recv(1024)
                print(f"Received response: {deserialise_request(response)}")
            except socket.timeout:
                print("Timeout: No response received")
            end_time = time.time()

            
            
            print(f"Round-trip time: {end_time - start_time} seconds")
        
        except socket.error as e: #Lots of these
            print(f"Socket error: {e}")
        except Exception as e:
            print(f"Other exception: {e}")





 ## can extend this out further since we've got communication between python and the go server working.

health = 150 # -> modify health for validation that data has transferred across
player = (1, 0, 1, 1, health, 1, 0, 0)  # default data 
send_request("127.0.0.1", 8000, 1, player)