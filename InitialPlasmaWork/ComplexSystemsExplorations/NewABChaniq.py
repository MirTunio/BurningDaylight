import numpy as np


counter = 0.0
total = 10000000
for i in np.arange(total):
    A = np.random.randint(1,11)
    B = np.random.randint(1,11)
    C = np.random.randint(1,11)
    
    if A>B and  B>C:
        counter += 1.0
    
print (counter/total) * 1000