
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
            pre_college =  (self.pre_college_experience[sport]['experience'], self.pre_college_experience[sport]['rating'])
        elif sport in self.im_experience:
            im = (self.im_experience[sport]['experience'], self.im_experience[sport]['rating'])
        if pre_college not empty and im not empty:
            return f'Pre-College: {pre_college}, IM: {im}'
        return 'No Experience'