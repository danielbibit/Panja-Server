class Rule(object):
    def __init__(self):
        self.events = []
        self.conditions = []
        self.actions = []
    
    def verify_if_true():
        for condition in conditions:
            if condition == False:
                return False
        
        return True

    def execute():
        for action in actions:
            action()