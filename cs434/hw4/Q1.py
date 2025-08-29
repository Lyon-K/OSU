import matplotlib.pyplot as plt
import numpy as np

x1 = np.arange(0, 31)
x2 = np.arange(0, 31)

plt.figure(figsize = (5, 5))

plt.vlines(x = 25, ymin = 0, ymax = 30, color = 'k')
plt.hlines(y = 15, xmin = 0, xmax = 30, color = 'k') 
plt.vlines(x = 5, ymin = 15, ymax = 30, color = 'k')
plt.vlines(x = 10, ymin = 0, ymax = 15, color = 'k')

plt.title('decision boundaries')
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.xlim(x1.min(), x1.max())
plt.ylim(x2.min(), x2.max())
plt.savefig('Q1a')