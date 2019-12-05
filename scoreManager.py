class ScoreManager:
    def __init__(self, players):
        self.__players = players
        
    def score(self, ball):
        """
            changes the score of the player that scored, based on the ball's owner
        """
        # if the ball was <= 0, then the score being changed is player 2's else it's player 1's
        affectedPlayer = self.__players[1] if ball.posX <= 10 else self.__players[0]
        # if the score was an own goal
        isOwnGoal = (ball.owner == affectedPlayer)
        # if the one scored against owned the ball, then they lose a point, else the other player gains a point
        if isOwnGoal:
            ball.owner.score -= 1
            affectedPlayer.score += 1
        else:
            affectedPlayer.score += 1
        
        # reset the ball's position
        ball.set_location(250, 250)
        ball.switch_owner(None)
        ball.launch()
        
