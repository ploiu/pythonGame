class ScoreManager:
    def __init__(self, players):
        self.__players = players
        
    def score(self, ball):
        """
            changes the score of the player that scored, based on the ball's owner
        """
        print('goal')
        print(ball.owner)
        # The player that gets the point
        scoringPlayer = self.__players[1] if ball.posX <= 10 else self.__players[0]
        # the player scored against
        otherPlayer = self.__players[1] if ball.posX > 10 else self.__players[0]
        print(scoringPlayer)
        # if the score was an own goal
        isOwnGoal = (ball.owner == otherPlayer)
        # if the one scored against owned the ball, then they lose a point as well as the scoring player getting a point
        if isOwnGoal:
            otherPlayer.score -= 1
        
        scoringPlayer.score += 1
        
        # reset the ball's position
        ball.set_location(250, 250)
        ball.switch_owner(None)
        ball.launch()
        
