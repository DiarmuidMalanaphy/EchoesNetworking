package main

import "fmt"

type game struct {
	ID        uint8
	playerMap map[uint16]player
}

func newGame(ID uint8) *game {
	g := game{
		ID:        ID,
		playerMap: make(map[uint16]player),
	}
	return &g
}

func (g game) addPlayer(p player) {
	g.playerMap[p.ID] = p
}

func (g *game) removePlayer(playerID uint16) {
	delete(g.playerMap, playerID)
	// Could cause problems because i'm not sure if that's deleting value or key.
}

func (g game) retrieveOpponents(playerID uint16) []player {
	players := []player{}
	for key, value := range g.playerMap {
		if key != playerID {
			players = append(players, value)
		}

	}
	fmt.Println(players)
	return players

}
