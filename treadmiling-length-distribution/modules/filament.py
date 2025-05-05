import numpy as np
from collections import deque
from modules.monomer import monomer

# MINUS END: append to the right (normal append)
# PLUS END: append to the left

class filament:
    def __init__(self):
        self.__monomers = deque()
    
    def add_monomer_minus_end(self, this_monomer: monomer):
        self.__monomers.append(this_monomer)
        
    def add_monomer_plus_end(self, this_monomer: monomer):
        self.__monomers.appendleft(this_monomer)
        
    def remove_monomer_minus_end(self):
        if len(self.__monomers) > 0:
            return self.__monomers.pop()
        elif len(self.__monomers) == 0:
            pass
        
    def remove_monomer_plus_end(self):
        if len(self.__monomers) > 0:
            return self.__monomers.popleft()
        elif len(self.__monomers) == 0:
            pass
    
    def swap_state(self, index):
        self.__monomers[index].change_state()
    
    @property
    def length(self):
        return len(self.__monomers)
    
    @property
    def num_T(self):
        return len([m for m in self.__monomers if m.state == "T"])
    
    @property
    def num_D(self):
        return len([m for m in self.__monomers if m.state == "D"])
    
    @property
    def monomers(self):
        return self.__monomers
    
    def filament_state(self):
        return [m.state for m in self.__monomers]
        
    
    
    