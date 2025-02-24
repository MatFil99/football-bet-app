

class BaseBetRule():

    def __init__(self, gain_pts=1, lose_pts=0):
        self.gain_pts = gain_pts
        self.lose_pts = lose_pts
        pass
        
    def win_bet(self, prediction, match):
        pass

    def score(self, prediction, match):
        total = 0
        if self.win_bet(prediction, match):
            total += self.gain_pts
        else:
            total -= self.lose_pts
        return total


class ExactResultRule(BaseBetRule):
    """
    predicted exact result of match
    """
    
    def win_bet(self, prediction, match):
        return prediction['home_score'] == match['home_score'] and prediction['away_score'] == match['away_score']


class GeneralResultRule(BaseBetRule):
    """
    predicted who wins or a draw
    """
        
    def win_bet(self, prediction, match):
        return (prediction['home_score'] - prediction['away_score']) * (match['home_score'] - match['away_score']) \
            or (prediction['home_score'] - prediction['away_score'] == 0 and (match['home_score'] - match['away_score'] == 0))


