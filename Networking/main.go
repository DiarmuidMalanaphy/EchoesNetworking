package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

// -> this standard will have to be relayed to the python too
const (
	RequestTypeUpdate             = uint8(1)
	RequestTypeInitialise         = uint8(2)
	RequestTypeGenerateGame       = uint8(3)
	RequestTypeGameInfo           = uint8(4)
	RequestTypeRemovePlayer       = uint8(5)
	RequestTypeUpdateProjectiles  = uint8(6)
	RequestTypeAddProjectile      = uint8(7)
	RequestTypeRemoveProjectiles  = uint8(8)
	RequestTypeRequestProjectiles = uint8(9)
	RequestTypeValidateServer     = uint8(10)

	RequestSuccessful = uint8(200)
	RequestFailure    = uint8(255)
)

func main() {

	i := newIndex()
	g := i.generateGame()

	ip, _ := getPublicIP()
	housekeepingCount := 0
	fmt.Println("Running on IP:", ip)
	// g2 := i.generateGame()
	// fmt.Println(*g)

	// fmt.Println(i.nextGameID)
	// fmt.Println(*g2)

	// p := i.addPlayer(999, 100, 100, 1)

	// fmt.Println(p)
	// fmt.Println(*g)
	//We create the player channel so the UDP listener goroutine can relay information back to main.
	// This significantly decreases the complexity.
	requestChannel := make(chan networkData)

	go listen(requestChannel)
	// go multipleSendTest()

	for {
		select {
		case req := <-requestChannel:

			// fmt.Printf("Received request type: %+v from %s\n", req.Request.Type, req.Addr)
			housekeepingCount++

			// Check if the housekeepingCount has reached 10
			if housekeepingCount >= 10 {
				// Call the housekeeping function
				i.houseKeeping()

				// Reset the housekeeping count
				housekeepingCount = 0
			}

			switch req.Request.Type {
			//The first type of event is where the user is updating their characters position.
			// -> We must return the position of all other characters.
			case RequestTypeUpdate:
				// essentially you feed the pointer to the buffer you want the binary data to be read,
				// if they send garbage it will crash actually
				var p player
				err := deserialiseData(req.Request.Payload, &p)

				if err != nil {
					fmt.Println(err)
					outgoingReq, _ := generateRequest(p, RequestFailure)
					sendUDP(req.Addr.String(), outgoingReq)

				}

				i.updatePlayer(p)
				// -> Generate a list of all enemies
				enemies := i.getPlayerEnemies(p)
				outgoingReq, _ := generateRequest(enemies, RequestSuccessful)

				sendUDP(req.Addr.String(), outgoingReq)

			case RequestTypeInitialise:
				var p player
				err := deserialiseData(req.Request.Payload, &p)
				if err != nil {
					fmt.Println(err)
					outgoingReq, _ := generateRequest(p, RequestFailure)
					sendUDP(req.Addr.String(), outgoingReq)
				}

				p = i.addPlayer(p.Health, p.XPosition, p.YPosition, p.Game)

				outgoingReq, _ := generateRequest(p, RequestSuccessful)
				sendUDP(req.Addr.String(), outgoingReq)

			case RequestTypeGenerateGame:
				//  -> Payload undefined for this, you could send literally whatever you want
				g = i.generateGame()
				outgoingReq, _ := generateRequest(g.ID, RequestSuccessful)
				// send back the game ID they've just generated
				sendUDP(req.Addr.String(), outgoingReq)

			case RequestTypeRemovePlayer:
				var p player
				err := deserialiseData(req.Request.Payload, &p)
				if err != nil {
					outgoingReq, _ := generateRequest(p.ID, RequestFailure)
					sendUDP(req.Addr.String(), outgoingReq)
					continue
				}

				i.deletePlayer(p.ID)
				outgoingReq, _ := generateRequest(p.ID, RequestSuccessful)
				sendUDP(req.Addr.String(), outgoingReq)

			case RequestTypeUpdateProjectiles:
				var p []projectile
				err := deserialiseData(req.Request.Payload, &p)
				if err != nil {
					outgoingReq, _ := generateRequest("pee", RequestFailure)
					sendUDP(req.Addr.String(), outgoingReq)
					continue
				}
				gameID := p[0].GameID
				playerID := p[0].PlayerID
				for _, proj := range p {
					i.updateProjectile(proj)
				}
				p = i.gameMap[gameID].getOpposingProjectiles(playerID)
				outgoingReq, _ := generateRequest(p, RequestSuccessful)

				sendUDP(req.Addr.String(), outgoingReq)

			case RequestTypeAddProjectile: //-> not as clear cut as adding humans, the projectiles are temporal.
				//-> doing a check to see if they've been added before within here

				var proj projectile
				err := deserialiseData(req.Request.Payload, &proj)
				if err != nil {
					outgoingReq, _ := generateRequest("bug", RequestFailure)
					sendUDP(req.Addr.String(), outgoingReq)
					continue
				}
				p := i.addProjectile(proj.PlayerID, proj.GameID, proj.Direction, proj.XPosition, proj.YPosition, proj.XVelocity, proj.YVelocity)

				outgoingReq, _ := generateRequest(p, RequestSuccessful)

				sendUDP(req.Addr.String(), outgoingReq)

			case RequestTypeRemoveProjectiles:
				var p []projectile
				err := deserialiseData(req.Request.Payload, &p)
				if err != nil {
					outgoingReq, _ := generateRequest("pee", RequestFailure)
					sendUDP(req.Addr.String(), outgoingReq)
					continue
				}
				for _, proj := range p {
					i.gameMap[proj.GameID].removeProjectile(proj.ProjectileID)
				}

				outgoingReq, _ := generateRequest(true, RequestSuccessful)

				sendUDP(req.Addr.String(), outgoingReq)

			case RequestTypeRequestProjectiles:
				var p player
				err := deserialiseData(req.Request.Payload, &p)
				if err != nil {
					outgoingReq, _ := generateRequest("pee", RequestFailure)
					sendUDP(req.Addr.String(), outgoingReq)
					continue
				}
				opposingProjectiles := i.gameMap[p.Game].getOpposingProjectiles(p.ID)
				outgoingReq, _ := generateRequest(opposingProjectiles, RequestSuccessful)

				sendUDP(req.Addr.String(), outgoingReq)

			case RequestTypeValidateServer: //Essentially a ping.
				outgoingReq, _ := generateRequest("pee", RequestSuccessful)
				sendUDP(req.Addr.String(), outgoingReq)

			}

		}
	}

}
func getPublicIP() (string, error) {
	resp, err := http.Get("https://api.ipify.org")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	ip, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	return string(ip), nil
}
