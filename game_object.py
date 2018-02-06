import json


class GameObject:
    setting = json.load(open('setting.json', 'r'))
    
    def __init__(self, master=None):
        self.master = master
        self.x = 0
        self.y = 0
        self.angle = 0
        self.color = []

    def repaint(self, screen):
        pass

    def update(self):
        pass

    def kill(self):
        pass

