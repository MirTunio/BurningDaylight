import numpy as np
from matplotlib import pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 16,12

final = np.array([])

for i in np.arange(1000):
    x = np.array([0])
    for i in np.arange(1600):
        if np.random.rand() > 0.5:
            x = np.append(x,x[-1:]+1)
        else:
            x = np.append(x,x[-1:]-1)
    final = np.append(final,x[-1:])
    plt.plot(x,'black',alpha=0.5)
plt.show()

plt.hist(final)
plt.show()
print('std = ' + str(np.std(final)))