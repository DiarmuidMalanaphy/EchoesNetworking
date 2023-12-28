from enum import Enum

class StandardFormats(Enum):
    Player = "=HHHHhBhh"
    Projectile = "=LHBHHhhh"
    RequestHeader = '=BI'