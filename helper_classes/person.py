
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

   def pre_college_experience_with(self, sport):
        if sport in self.pre_college_experience:
            pre_college = (self.pre_college_experience[sport]['experience'],
                           self.pre_college_experience[sport]['rating'])
            return pre_college
        return None

    def im_experience_with(self, sport):
        if sport in self.im_experience:
            im = (self.im_experience[sport]['experience'],
                  self.im_experience[sport]['rating'])
            return im
        return None
