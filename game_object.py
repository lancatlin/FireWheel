import json


class GameObject:
    setting = json.load(open('setting.json', 'r'))
    
    def repaint(self, screen):
        pass

    def update(self):
        pass

    def kill(self):
        pass

