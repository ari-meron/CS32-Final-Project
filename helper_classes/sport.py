
class Sport():
    
    def __init__(self, name, size, very_compatible, somewhat_compatible):
        self.name = name
        self.size = size
        self.very_compatible = very_compatible
        self.somewhat_compatible = somewhat_compatible

    def get_tier(self, sport):
        if sport in self.very_compatible:
            return "very"
        elif sport in self.somewhat_compatible:
            return "somewhat"
        else:
            return "not"



