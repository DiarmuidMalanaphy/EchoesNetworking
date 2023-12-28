package main

type projectile struct {
	ProjectileID uint32
	PlayerID     uint16
	GameID       uint8
	XPosition    uint16
	YPosition    uint16
	Direction    int16
	XVelocity    int16
	YVelocity    int16
}

func newProjectile(projectileID uint32, playerID uint16, gameID uint8, xPosition uint16, yPosition uint16, direction int16, xVelocity int16, yVelocity int16) projectile {
	p := projectile{
		ProjectileID: projectileID,
		PlayerID:     playerID,
		GameID:       gameID,
		XPosition:    xPosition,
		YPosition:    yPosition,
		Direction:    direction,
		XVelocity:    xVelocity,
		YVelocity:    yVelocity,
	}
	return p
}
