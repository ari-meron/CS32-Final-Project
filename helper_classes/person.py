
class Person():

    def __init__(self, name, varsity, pre_college_experience, im_experience):

        self.name = name
        self.varsity = varsity
        self.pre_college_experience = pre_college_experience
        self.im_experience = im_experience

    def is_banned(self, sport):
        if self.varsity == sport:
            return True
        return False

    def experience_with(self, sport):
        if sport in self.pre_college_experience:
            return (self.pre_college_experience[sport]['experience'], self.pre_college_experience[sport]['rating'])