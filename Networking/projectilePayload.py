class ProjectilePayload:
    def __init__(self, ProjectileID=0, PlayerID=0, GameID=0, XPosition=0, YPosition=0, Direction=0, XVelocity=0, YVelocity=0):
        self.ProjectileID = ProjectileID
        self.PlayerID = PlayerID
        self.GameID = GameID
        self.XPosition = XPosition
        self.YPosition = YPosition
        self.Direction = Direction
        self.XVelocity = XVelocity
        self.YVelocity = YVelocity

    def update(self, new_info_tuple):
        # Update the projectile's attributes based on the tuple
        self.ProjectileID, self.PlayerID, self.GameID, self.XPosition, self.YPosition, self.Direction, self.XVelocity, self.YVelocity = new_info_tuple

    def to_tuple(self):
        return (self.ProjectileID, self.PlayerID, self.GameID, self.XPosition, self.YPosition, self.Direction, self.XVelocity, self.YVelocity)

    @staticmethod
    def from_tuple(data_tuple):
        """
        Create a ProjectilePayload object from a tuple.

        :param data_tuple: A tuple containing projectile data in the order:
                           (ProjectileID, PlayerID, GameID, XPosition, YPosition, Direction, XVelocity, YVelocity)
        :return: A ProjectilePayload object initialized with the provided data.
        """
        if len(data_tuple) != 8:
            raise ValueError("Tuple must have exactly 8 elements")

        return ProjectilePayload(*data_tuple)
    @classmethod
    def from_projectile(cls, projectile):
        """
        Create a ProjectilePayload object from a Projectile object.

        :param projectile: A Projectile object.
        :return: A ProjectilePayload object initialized with data from the Projectile object.
        """
        return cls(
            ProjectileID=projectile.ID,
            PlayerID=projectile.player.internetID if projectile.player else 0,
            GameID=projectile.player.gameID if projectile.player else 0,
            XPosition=round(projectile.position.x),
            YPosition=round(projectile.position.y),
            Direction=round(projectile.player.movementFacing) if projectile.player else 0,
            XVelocity=round(projectile.velocity.x),
            YVelocity=round(projectile.velocity.y)
        )