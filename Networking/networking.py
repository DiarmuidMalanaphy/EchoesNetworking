import socket
import struct
import time
from playerPayload import PlayerPayload

from requestType import RequestType


class Networking:
    def __init__(self,hostIP,hostPort = 8000):
        self.hostIP = hostIP
        self.hostPort = hostPort


    


    

    def send_update_player_request(self,player):
        # player_data = self.serialise_player(player)
        _,player_data = self.serialize_payload(player,"=HBHHhBhh")
        response = self.__send_general_payload_request(RequestType.UpdatePlayer.value,player_data)
        
        payload = self.deserialise_player(response)
        for enemy in payload:
            print(player[0],"'s enemy is ",enemy[0])

    def send_initialise_player_request(self,player):
        # player_data = self.serialise_player(player)
        _,player_data = self.serialize_payload(player,"=HBHHhBhh")
        response = self.__send_general_payload_request(RequestType.InitialisePlayer.value,player_data)
        
        
        payload = self.deserialise_player(response)
        
        return(payload)
    
    def __send_general_payload_request(self,request_type,payload):
        # for more extensive documentation read __send_player_request
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                
                # Payload length (int32)
                # We have to put self in on the python side as we need it for serialisation on go-side
                # Holy shit this was a pain in the ass, spent ages on wireshark figuring out that
                # 4 bytes were missing and what they were
                # Was the payload length 

                # It's to do with the way binarisation works in go, you have to define a fixed size because binarisation does not like unknown sized onjects
                # for generalisation i had to make the payload an undefined size in go, but i have to keep a standard.
                payload_length = len(payload)
                request_data = struct.pack('=BI', request_type, payload_length) + payload
                # 'B' for request type (uint8) and 'I' for payload length (int32)
                sock.sendto(request_data, (self.hostIP, self.hostPort))
                start_time = time.time()
                try:
                    response = sock.recv(1024)
                    end_time = time.time()
            
                    print(f"Round-trip time: {end_time - start_time} seconds")
                    
                    
                    return(response)
                    
                except socket.timeout:
                    print("Timeout: No response received")
                

            except socket.error as e:
                print(f"Socket error: {e}")
            except Exception as e:
                print(f"Other exception: {e}")
                
                




    def serialise_player(self, player):
        return struct.pack('=HBHHhBhh', *player)
    
    
    

    def serialize_payload(self,payload, format_string):
        # Ensure the format string starts with '='
        if not format_string.startswith('='):
            format_string = '=' + format_string

        try:
            # Convert payload to tuple if it has a to_tuple method
            if hasattr(payload, 'to_tuple'):
                payload = payload.to_tuple()

            # Serialize the payload
            serialized_data = struct.pack(format_string, *payload)

            # Calculate and return payload length and serialized data
            payload_length = len(serialized_data)
            return payload_length, serialized_data

        except struct.error as e:
            raise ValueError(f"Payload does not match format '{format_string}': {e}")
        


    def deserialize_payload(serialized_data, single_item_format):
        # Ensure the format string starts with '='
        if not single_item_format.startswith('='):
            single_item_format = '=' + single_item_format

        # Calculate the size of a single item
        item_size = struct.calcsize(single_item_format)
        
        # Initialize an empty list to store unpacked items
        items = []

        # Iterate over the serialized data and unpack each item
        for i in range(0, len(serialized_data), item_size):
            # Extract a chunk of data for a single item
            item_data = serialized_data[i:i + item_size]

            try:
                # Unpack the item and append to the list
                unpacked_item = struct.unpack(single_item_format, item_data)
                items.append(unpacked_item)
            except struct.error as e:
                raise ValueError(f"Error unpacking data: {e}")

        return items
    


    def deserialise_request(self, request_data):
        # Unpack the first 5 bytes for Type and payloadLength
        
        type, payload_length = struct.unpack('=BI', request_data[:5])

        # Extract the payload using the payload_length
        payload = request_data[5:5+payload_length]

        return (type, payload_length, payload)

    

    def deserialise_player(self, data):
        format_string = '=HBHHhBhh'
        
        type, _ , payload = self.deserialise_request(data)
        #print(type)
        
        players = []
        if type == 200:  # Replace 200 with the actual type you're checking for
            # Calculate the size of a single player's data
            player_size = struct.calcsize(format_string)

            # Iterate over the payload in chunks of player_size
            for i in range(0, len(payload), player_size):
                # Extract a chunk of player data
                player_data = payload[i:i + player_size]
                # Unpack and append the player data to the list
                unpacked_data = struct.unpack(format_string, player_data)
                players.append(unpacked_data)

            return players
        return(None)
    

if __name__ == "__main__":
    health = 1 # -> modify health for validation that data has transferred across
    player1 = PlayerPayload(1,100,100,health,1)  # default data 
    health = 2 # -> modify health for validation that data has transferred across
    player2 = PlayerPayload(2,100,100,health,1)  # default data 
    print(player2.health)


    networkingTool = Networking("127.0.0.1")
    player1 = networkingTool.send_initialise_player_request(player1)[0]
    
    
    
    
    player2 = networkingTool.send_initialise_player_request(player2)[0]
    
    
    networkingTool.send_update_player_request(player2)
    

    networkingTool.send_update_player_request(player1)

