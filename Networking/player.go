package main

type player struct {
	ID        uint16
	Direction uint16
	XPosition uint16
	YPosition uint16
	Health    int16
	Game      uint8
	XVelocity int16
	YVelocity int16
}

// ID -> identifies each player within a game / globally. -> might not require this as each user is identified by their position in a hashmap.
// xPosition, yPosition -> indicates where each player should start.
// health -> indicates the starting health of a player.
// game -> indicates the game the player is playing in -> This is in the event there are several instanced games.

func newPlayer(ID uint16, xPosition uint16, yPosition uint16, health int16, game uint8) player {

	p := player{
		ID:        ID,
		Direction: 0,
		XPosition: xPosition,
		YPosition: yPosition,
		Health:    health,
		Game:      game,
		XVelocity: 0,
		YVelocity: 0,
	}
	return p

}
