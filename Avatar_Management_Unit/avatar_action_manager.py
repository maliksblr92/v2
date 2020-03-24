

#connect this class to the avatar ess apis to perform these actions



class Avatar_Action(object):

    username = None
    password = None
    social_media = None

    def __init__(self,username,password,social_media='facebook'):
        self.username = username
        self.password = password
        self.social_media = social_media



    def post(self,text,image=''):
        pass

    def comment(self,text,target_post_url):
        pass

    def react(self,reaction,target_post_url):
        pass

    def share(self,text,target_post_url):
        pass


#beta class for perforing or processing the actions instaed of into the task

class Perform_Action(object):

    def __init__(self):
        pass


