import matplotlib.pyplot as plt
import numpy as np

# --- Torus parameters ---
R = 5  # major radius
r = 1  # minor radius

# --- Rectangle size (your fundamental domain) ---
W = 4
H = 4


# --- Draw torus surface ---
def draw_torus(ax):
    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, 2 * np.pi, 30)
    u, v = np.meshgrid(u, v)

    X = (R + r * np.cos(v)) * np.cos(u)
    Y = (R + r * np.cos(v)) * np.sin(u)
    Z = r * np.sin(v)

    ax.plot_surface(X, Y, Z, alpha=0.2, edgecolor='none', zorder=-1)

# --- Torus mapping --
def rect_to_torus(x, y, scale = 1.0):
    u = 2 * np.pi * (x / W)
    v = 2 * np.pi * (y / H)

    X = (R + (r * np.cos(v))*scale) * np.cos(u)
    Y = (R + (r * np.cos(v))*scale) * np.sin(u)
    Z = r * np.sin(v)

    return X, Y, Z

# --- Draw one segment ---
def draw_segment(ax, p1, p2, color='blue'):
    t = np.linspace(0, 1, 200)

    x = p1[0] + t * (p2[0] - p1[0])
    y = p1[1] + t * (p2[1] - p1[1])

    X, Y, Z = rect_to_torus(x, y)
    ax.plot(X, Y, Z, color=color, linewidth=5, zorder=5)


## --- Draw one point ---
def draw_point(ax, p, color='black', size=30, label=None):
    """
    Plots a 2D coordinate (x, y) onto the 3D torus surface.
    """
    # Convert the 2D point from the rectangle to 3D torus space
    X, Y, Z = rect_to_torus(p[0], p[1])

    # Plot the point. zorder=10 keeps it on top of the surface mesh.
    ax.scatter(X, Y, Z, color=color, s=size, edgecolors='white', linewidth=1, label=label)


# --- YOUR DRAWING HERE ---
segments = [
    # vertex 1
    ((1, 1), (1, 3-H)),
    ((1, 1), (2, 3)),
    ((1, 1), (3-W, 3-H)),
    ((1, 1), (4-W, 3-H)),
    # # vertex 2
    ((2, 1), (1, 3-H)),
    ((2, 1), (2, 3)),
    ((2, 1), (3, 3)),
    ((2, 1), (4, 3)),
    # # vertex 3
    ((3, 1), (1, 3-H)),
    ((3, 1), (2, 3-H)),
    ((3, 1), (3, 3-H)),
    ((3, 1), (4, 3)),
    # # vertex 4
    ((4-W, 1), (1, 3)),
    ((4-W, 1), (2, 3)),
    ((4, 1), (3, 3-H)),
    ((4, 1), (4, 3))
]


colors = ['red', 'green', 'blue', 'purple', 'cyan', 'magenta', 'yellow']

# --- Plot ---
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(projection='3d')



draw_point(ax, segments[0][0], label='1')
draw_point(ax, segments[1*4][0], label='2')
draw_point(ax, segments[2*4][0], label='3')
draw_point(ax, segments[3*4][0], label='4')
draw_point(ax, segments[0][1])
draw_point(ax, segments[1*4+1][1])
draw_point(ax, segments[2*4+2][1])
draw_point(ax, segments[3*4+3][1])

# Cycle through the colors list for all 16 segments
for i, seg in enumerate(segments):
    col = colors[i % len(colors)] # This will repeat the 4 colors
    draw_segment(ax, seg[0], seg[1], col)

draw_torus(ax)

# nicer view
ax.set_box_aspect([4, 4, 1])
ax.axis('off')

plt.show()
