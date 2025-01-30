import json

class match_log:
    # decklist - Name of decks played in match
    # match_result - 1 is winner , 0 are losers example deck1 wins in 4 player -> match_result = [1,0,0,0]
    # group_id match_logged for a specific playgroup - if not specified it is group 0 by default
    def __init__(self, decklist = None, match_result = None, group_id = None):
        self.decklist = decklist if decklist is not None else []  
        self.match_result = match_result if match_result is not None else generate_match_result(len(decklist))
        self.group_id = group_id if group_id is not None else 0

    def to_dict(self):
        """
        Converts the match log object to a dictionary.
        """
        return {
            "decklist": self.decklist,
            "match_result": self.match_result,
            "group_id": self.group_id
        }


# Default first deck in decklist wins
def generate_match_result (participant_number, position = None):
    match_result = []
    if participant_number < 1:
        return match_result
    else:
        match_result.append(1)
        for i in range(participant_number-1):
            match_result.append(0)
    if position is not None:
        if position >= participant_number:
            raise IndexError
        match_result[0] = 0
        match_result[position] = 1
    return match_result