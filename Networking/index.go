package main

import "fmt"

// I bundled the logic for creating IDs within the indexing logic because they make a lot of sense together -> I'll have to synchronise
// The addplayer function

type index struct {
	playerMap    map[uint16]player
	nextPlayerID uint16
	gameMap      map[uint8]*game
	nextGameID   uint8
}

func newIndex() *index {
	i := index{
		playerMap:    make(map[uint16]player),
		nextPlayerID: 1,
		gameMap:      make(map[uint8]*game),
		nextGameID:   1,
	}
	return &i
}

// When you create a player you give the player a unique id and then create an instance of player
// ID Generation is really simplistic -> 1. create a counter 2. increment counter, this would have to be modified if the servers were distributed but they're not.

// Whenever we generate a player they have to be assigned a game
func (i *index) addPlayer(health int16, xPosition uint16, yPosition uint16, gameID uint8) player {
	// error checks
	// -> game doesn't exist.
	// -> health below zero

	p := newPlayer(i.nextPlayerID, xPosition, yPosition, health, gameID)

	i.playerMap[i.nextPlayerID] = p
	i.nextPlayerID = i.nextPlayerID + 1

	i.gameMap[gameID].addPlayer(p) // Giving the player a position within a game.
	return (p)
}

func (i *index) addProjectile(playerID uint16, gameID uint8, direction int16, xPosition uint16, yPosition uint16, xVelocity int16, yVelocity int16) projectile {
	gameInstance := i.gameMap[gameID]

	p := gameInstance.addProjectile(playerID, direction, xPosition, yPosition, xVelocity, yVelocity)
	return p
}

func (i *index) deletePlayer(playerID uint16) {
	// Check if the player exists in the playerMap
	if player, exists := i.playerMap[playerID]; exists {
		// Delete the player from the playerMap
		delete(i.playerMap, playerID)

		// Delete the player from the corresponding game's playerMap
		if game, gameExists := i.gameMap[player.Game]; gameExists {
			delete(game.playerMap, playerID)
		} else {
			fmt.Printf("Game with ID %d not found for player\n", player.Game)
		}
	} else {
		// Handle the case where the player doesn't exist
		fmt.Printf("Player with ID %d not found\n", playerID)
	}
}

func (i *index) updatePlayer(updatedPlayer player) {
	// Check if the player exists in the playerMap
	if _, exists := i.playerMap[updatedPlayer.ID]; exists {
		// Replace the old player with the updated player in the map
		i.playerMap[updatedPlayer.ID] = updatedPlayer
		i.gameMap[updatedPlayer.Game].playerMap[updatedPlayer.ID] = updatedPlayer
	} else {
		// Handle the case where the player doesn't exist
		fmt.Printf("Player with ID %d not found\n", updatedPlayer.ID)
	}
}

func (i *index) updateProjectile(updatedProjectile projectile) {
	// Assuming you have a map for projectiles similar to playerMap
	// Check if the projectile exists
	if _, exists := i.gameMap[updatedProjectile.GameID].projectileMap[updatedProjectile.ProjectileID]; exists { //projectileMap[updatedProjectile.ProjectileID]; exists {
		// Update the projectile in the projectileMap
		// i.projectileMap[updatedProjectile.ProjectileID] = updatedProjectile
		i.gameMap[updatedProjectile.GameID].projectileMap[updatedProjectile.ProjectileID] = updatedProjectile
		// If you also store projectiles in a game-specific map or any other structure, update it there as well
		// i.gameMap[updatedProjectile.Game].projectileMap[updatedProjectile.ProjectileID] = updatedProjectile
	} else {
		// Handle the case where the projectile doesn't exist
		fmt.Printf("Projectile with ID %d not found\n", updatedProjectile.ProjectileID)
	}
}

func (i *index) changePlayerGame(p player, newGameID uint8) { //Might have to pass p by reference.
	//error checks
	// -> Game doesn't exist
	// -> Player doesn't exist

	// Deleting the player from their original game
	// bit convoluted but we go through the index to the game and then delete the player from that playermap.
	delete(i.gameMap[p.Game].playerMap, p.ID)

	// putting the player in the new player map.
	i.gameMap[newGameID].playerMap[p.ID] = p

	//Assigning the player their new game

	p.Game = newGameID

}

func (i *index) getPlayerEnemies(p player) []player {
	//game already has the function defined so it's a matter of getting the game the user is in
	return (i.gameMap[p.Game].retrieveOpponents(p.ID))
}

func (i *index) generateGame() *game {
	g := newGame(i.nextGameID)
	i.gameMap[i.nextGameID] = g
	i.nextGameID = i.nextGameID + 1
	return g

}

func (i index) deleteGame() {
	// -> This is going to be fucked, i need to decide if this deletes the players too.
	// -> interesting design choice -> player being in game 0 means they go to lobby.
}
