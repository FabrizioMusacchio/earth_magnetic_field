"""
A script to plot the Earth's magnetic field as a vector field.

author: Fabrizio Musacchio (fabriziomusacchio.com)
date: August 17, 2020

ACKNOWLEDGEMENT:
The code is modified after https://scipython.com/blog/visualizing-the-earths-magnetic-field/
"""
# %% IMPORTS
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
# %% MAIN
# define some constants:
B0 = 3.12e-5 # Mean magnitude of the Earth's magnetic field at the equator in T:
RE = 6.370  # Radius of Earth, Mm (10^6 m: mega-metres!)
alpha = np.radians(9.6) # Deviation of magnetic pole from axis

# define the magnetic field vector B(r, theta) in polar coordinates:
def B(r, theta):
    """Return the magnetic field vector at (r, theta)."""
    fac = B0 * (RE / r)**3
    return -2 * fac * np.cos(theta + alpha), -fac * np.sin(theta + alpha)

# grid of x, y points on a Cartesian grid:
nx, ny = 64, 64
XMAX, YMAX = 40, 40
x = np.linspace(-XMAX, XMAX, nx)
y = np.linspace(-YMAX, YMAX, ny)
X, Y = np.meshgrid(x, y)
r, theta = np.hypot(X, Y), np.arctan2(Y, X)

# magnetic field vector, B = (Ex, Ey), as separate components:
Br, Btheta = B(r, theta)

# transform to Cartesian coordinates:
c, s = np.cos(np.pi/2 + theta), np.sin(np.pi/2 + theta)
Bx = -Btheta * s + Br * c
By = Btheta * c + Br * s


# plot:
fig, ax = plt.subplots(figsize=(8, 8))
ax.streamplot(x, y, Bx, By, color="aqua", linewidth=1, cmap=plt.cm.binary,
              density=2, arrowstyle='->', arrowsize=1.5)
ax.add_patch(Circle((0, 0), RE, color='darkgray', zorder=100))
ax.set_facecolor('black')
# Add Earth's geographic and magnetic pole axis (straight vertical)
ax.plot([0, 0], [-YMAX, YMAX], '-', c="pink",linewidth=3)
x_magnetic = np.array([-YMAX, YMAX])
y_magnetic = x_magnetic * np.tan(np.pi/2-alpha )
ax.plot(x_magnetic, y_magnetic, 'y-', linewidth=3)
ax.set_xlabel('$x$ in 10$^6$ m')
ax.set_ylabel('$y$ in 10$^6$ m')
ax.set_xlim(-XMAX, XMAX)
ax.set_ylim(-YMAX, YMAX)
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig('earths_magnetic_field.png', dpi=300)
plt.show()

# %% END