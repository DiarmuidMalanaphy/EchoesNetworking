from enum import Enum

class RequestType(Enum):
    
    UpdatePlayer  = 1
    InitialisePlayer = 2
    InitialiseGame = 3
    RequestSuccessful = 200