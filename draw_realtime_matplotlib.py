
import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 100, 0, 10])
plt.ion()  # in order to enable interactive plotting

for i in range(100):
    y = np.random.random() * 10
    plt.scatter(i, y)
    plt.pause(0.05)  # to both draw the new data and it runs the GUI's event loop (allowing for mouse interaction).

plt.pause(4)
