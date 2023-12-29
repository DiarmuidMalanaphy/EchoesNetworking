from enum import Enum

class RequestType(Enum):
    
    UpdatePlayer  = 1
    InitialisePlayer = 2
    InitialiseGame = 3
    GetGameInfo = 4
    RemovePlayer = 5
    UpdateProjectiles = 6
    InitialiseProjectile = 7
    RemoveProjectiles = 8
    RequestProjectileInformation = 9
    ValidateServer = 10
    RequestSuccessful = 200
    RequestFailed = 255