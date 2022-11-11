import numpy as np
import matplotlib.pyplot as plt


n_points = 10
aa = np.linspace(0, 10, n_points)
bb = np.linspace(0, 3, n_points)

def cost(a, b):
    return a + b

z = []
for a in aa:
    for b in bb:
        z.append(cost(a, b))

z = np.reshape(z, [len(aa), len(bb)])

fig, ax = plt.subplots()
im = ax.pcolormesh(aa, bb, z, cmap='hot')
fig.colorbar(im)

ax.axis('tight')
plt.show()
