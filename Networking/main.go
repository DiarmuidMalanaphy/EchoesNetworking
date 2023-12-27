package main

import (
	"fmt"
	"os"
)

// -> this standard will have to be relayed to the python too
const (
	RequestTypeUpdate       = uint8(1)
	RequestTypeInitialise   = uint8(2)
	RequestTypeGenerateGame = uint8(3)
	RequestSuccessful       = uint8(200)
)

func main() {

	i := newIndex()
	g := i.generateGame()
	// g2 := i.generateGame()
	fmt.Println(*g)

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

			switch req.Request.Type {
			//The first type of event is where the user is updating their characters position.
			// -> We must return the position of all other characters.
			case RequestTypeUpdate:
				players, err := deserialisePlayers(req.Request.Payload)
				if err != nil {
					fmt.Println(err)
					os.Exit(1)
				}
				if len(players) > 1 {
					fmt.Println("Too many inputs for an update")
					break
				}
				player := players[0]
				fmt.Println(player.Health) // I've been using the health as an indicator to prove that we've selected the correct person.
				// -> Generate a list of all enemies
				enemies := i.getPlayerEnemies(player)
				outgoingReq, _ := generateRequest(enemies, RequestSuccessful)
				address := req.Addr.String()
				fmt.Println(address)
				fmt.Println(*g)
				sendUDP(req.Addr.String(), outgoingReq)

			case RequestTypeInitialise:
				players, err := deserialisePlayers(req.Request.Payload)
				if err != nil {
					fmt.Println(err)
					os.Exit(1)
				}
				if len(players) > 1 {
					fmt.Println("Too many players to initialise")
					break
				}
				p := players[0]
				p = i.addPlayer(p.Health, p.XPosition, p.YPosition, p.Game)
				generatedPlayer := make([]player, 1)
				generatedPlayer[0] = p
				outgoingReq, _ := generateRequest(generatedPlayer, RequestSuccessful)
				sendUDP(req.Addr.String(), outgoingReq)

			case RequestTypeGenerateGame:
				//  -> Payload undefined for this, you could send literally whatever you want
				g = i.generateGame()
				// g.
			}

		}
	}

}
