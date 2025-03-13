import numpy as np

class filament:
    def __init__(self, length, dt_react):
        self.__length = length
        self.__t_tail = 0
        self.__dt_react = dt_react
        self.is_depolymerized = False
        self.is_polymerized = False
    
    def grow(self, r_on):
        p_on = r_on * self.__dt_react
        r = np.random.uniform()
        if r < p_on:
            self.__length += 1
            self.is_polymerized = True
    
    def shrink(self, tau_det):
        p_off = 1 - np.exp(-self.__dt_react / tau_det)
        r = np.random.uniform()
        if r < p_off:
            self.__length -= 1
            self.__t_tail = 0
            self.is_depolymerized = True
    
    def depolymerize(self, tau_det):
        p_off = 1 - np.exp(-self.__dt_react / tau_det)
        r = np.random.uniform()
        if r < p_off:
            self.is_depolymerized = True
        
    
    def age_up_tail(self):
        self.__t_tail += self.__dt_react
    
    @property
    def length(self):
        return self.__length
    
    @property
    def t_tail(self):
        return self.__t_tail
        