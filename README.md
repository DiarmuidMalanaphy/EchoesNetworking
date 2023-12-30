# Project Name: Echoes Networking
## Introduction

This project extends a simple game, originally developed over a weekend, where players navigate a miner through a cave. The new extension incorporates a Golang server to enable local multiplayer across a local network and internet multiplayer for global crossplay.

The motivation behind this extension was to test a low-memory-usage backend for a larger upcoming project. Golang was chosen for its efficiency in memory usage and effectiveness in web development, aligning with the goals of creating a scalable and robust multiplayer experience.

## Technologies & Frameworks Used
- **Server**: Golang
- **Client**: Python
- **API**: Custom built - handles requests for player information, game information and server aliveness.

## Features
- Local and Global Multiplayer.
- Player Vs Player (PVP) combat.


## Installation & Setup
### Prerequisites
  To run the server:
    - You must have Golang installed. Visit [Golang Installation](https://go.dev/doc/install) for instructions.
    
  To run the game:
    - You must have Python installed. Visit [Python Downloads](https://www.python.org/downloads/) for instructions.

  To access the code:
    - git clone https://github.com/DiarmuidMalanaphy/EchoesNetworking
  ### Setting up the game

Follow these steps to set up the project:

The Game follows a Client-Server Model.

#### Setting up the server.

   **Local Multiplayer** - Run the server and play across the same local network.
   
1. Run the bat or bash script "runServer"
2. The terminal should display a local IP address, this is what you will need to type in to find the lobby later on.
   
   **Global Multiplayer** - Run the server and play across the internet.
   
1. The server computer will have to enable portforwarding to port 8000 on the local machine. There are guides online, here is one https://www.wikihow.com/Set-Up-Port-Forwarding-on-a-Router.
2. Run the bat or bash script "runServer"
3. The terminal should display a public IP address, this is what you will need to type in to find the lobby later on.

#### Playing the game.

1. Ensure a server is running, only one server has to be running.
2. Run the bat or bash script runGame
3. Follow the user interface.

## API Documentation

## Networking Class (Python)

### Description

- **Manages game and player states**, comprehensive API that facilitates server-client communication for a game, involving player and projectile interactions.

### Player Interaction
- `send_initialise_player_request`: **Initializes a player** and returns player data.
- `send_update_player_request`: **Updates a player's data** and retrieves a list of enemies.
- `send_remove_player_request`: **Removes a player** and returns a confirmation payload.
### Game Interaction
- `send_initialise_game_request`: **Initializes a game** and returns a game ID.

### Projectile Interaction
- `send_initialise_projectile_request`: **Initializes a projectile**.
- `send_update_projectiles_request`: **Updates multiple projectiles** similar to update_player_request.
- `send_request_projectiles_request`: **Requests all projectiles** for a player when the user doesn't have any projectiles to send.
- `send_remove_projectile_request`: **Removes projectiles**.
### Server Validation
- `send_validate_server_request`: Checks **server availability**.

## Enums

### StandardFormats
- Defines **data formats** for players, projectiles, and request headers.

### RequestType
- Enumerates various **request types**, including player updates, game initialization, and projectile management.



