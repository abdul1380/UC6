nPop=2400
pc=0.8
nc=2*round(pc*nPop/2)
print(nc)
import numpy.matlib as m
class empty_individual:
    def __init__(self): 
        self.Position =[0]
        self.Cost = [0]
        
    
     
    
obj = empty_individual()
a=([],[])
a2 = m.repmat([obj.Position,obj.Cost], 4,2)
print(a)
print(a2)


