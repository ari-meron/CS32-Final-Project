
class Person():

    def __init__(self, name, varsity, pre_college_experience, im_experience):

        self.name = name
        self.pre_college_experience = pre_college_experience
        self.im_experience = im_experience

    def is_banned(sport):
        if varsity == sport:
            return True
        return False

    def experience_with(sport):
        if sport in pre_college_experience:
            return (pre_college_experience[sport]['experience'], pre_college_experience[sport]['rating'])