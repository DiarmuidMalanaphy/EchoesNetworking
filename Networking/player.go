package main

type player struct {
	ID        uint16
	Direction uint8
	xPosition uint16
	yPosition uint16
	health    int16
	game      uint8
	xVelocity int16
	yVelocity int16
}

// ID -> identifies each player within a game / globally. -> might not require this as each user is identified by their position in a hashmap.
// xPosition, yPosition -> indicates where each player should start.
// health -> indicates the starting health of a player.
// game -> indicates the game the player is playing in -> This is in the event there are several instanced games.

func newPlayer(ID uint16, xPosition uint16, yPosition uint16, health int16, game uint8) player {

	p := player{
		ID:        ID,
		Direction: 0,
		xPosition: xPosition,
		yPosition: yPosition,
		health:    health,
		game:      game,
		xVelocity: 0,
		yVelocity: 0,
	}
	return p

}
