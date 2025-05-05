class monomer:
    def __init__(self, state):
        self.__state = state
        
    def change_state(self):
        if self.__state == "T":
            self.__state = "D"
        elif self.__state == "D":
            self.__state = "T"
        else:
            raise ValueError("Invalid state. State must be either 'T' or 'D'.")
        
    @property
    def state(self):
        return self.__state