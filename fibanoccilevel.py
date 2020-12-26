
class FibannociLevel():
    
    def __init__(self,support,resistance,level0,level1,level2,level3):
        self.support = support
        self.resistance = resistance
        self.level0 = level0
        self.level1 = level1
        self.level2 = level2
        self.level3 = level3
    
    def __init__(self):
        self.support = 0
        self.resistance = 0
   

    
    def print_content(self):
        print('support =' + str(self.support))
        print('resistance = ' +  str(self.resistance) )
        print('level 0 =' + str(self.level0))
        print('level 1 = ' + str(self.level1 ))
        print('level 2 =' + str(self.level2))
        print('level 3 = ' + str(self.level3 ))
