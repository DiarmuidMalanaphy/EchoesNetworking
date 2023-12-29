package main

import "fmt"

type game struct {
	ID               uint8
	playerMap        map[uint16]player
	projectileMap    map[uint32]projectile
	nextProjectileID uint32
}

func newGame(ID uint8) *game {
	g := game{
		ID:               ID,
		playerMap:        make(map[uint16]player),
		projectileMap:    make(map[uint32]projectile),
		nextProjectileID: 1,
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

func (g *game) addProjectile(playerID uint16, direction int16, xPosition uint16, yPosition uint16, xVelocity int16, yVelocity int16) projectile {
	p := newProjectile(g.nextProjectileID, playerID, g.ID, xPosition, yPosition, direction, xVelocity, yVelocity)
	g.projectileMap[g.nextProjectileID] = p
	g.nextProjectileID = g.nextProjectileID + 1 // Increment nextProjectileID

	return p
}

func (g *game) removeProjectile(projectileID uint32) {
	delete(g.projectileMap, projectileID)
	// Could cause problems because i'm not sure if that's deleting value or key.
}

func (g game) retrieveOpponents(playerID uint16) []player {
	players := []player{}
	for key, value := range g.playerMap {
		if key != playerID {
			players = append(players, value)
		}

	}

	return players

}

func (g game) getOpposingProjectiles(playerID uint16) []projectile {
	opposingProjectiles := []projectile{}
	for _, proj := range g.projectileMap {
		if proj.PlayerID != playerID {
			opposingProjectiles = append(opposingProjectiles, proj)
		}
	}
	fmt.Println(opposingProjectiles)
	return opposingProjectiles
}
