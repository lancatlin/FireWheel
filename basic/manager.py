class Manager:
    def __init__(self, master=None):
        self.master = master
        self.list = set()
        
    def callUpdate(self):
        for i in self.list:
            i.callUpdate()

    def callRepaint(self, screen, pos):
        for i in self.list:
            i.callRepaint(screen, pos)

