import matplotlib.pyplot as plt
import numpy as np

# --- Parameters ---
R, r = 5, 1
W, H = 4, 4


# --- Mapping with r_offset for "hover" ---
def rect_to_torus(x, y, scale = 1.0):
    u = 2 * np.pi * (x / W)
    v = 2 * np.pi * (y / H)

    X = (R + (r * np.cos(v))*scale) * np.cos(u)
    Y = (R + (r * np.cos(v))*scale) * np.sin(u)
    Z = r * np.sin(v)

    return X, Y, Z


# --- Chunked Torus Spine ---
def draw_torus_spine(ax, chunks=40):
    theta = np.linspace(0, 2 * np.pi, 400)
    X_full = R * np.cos(theta)
    Y_full = R * np.sin(theta)
    Z_full = np.zeros_like(theta)

    size = len(theta) // chunks
    for i in range(chunks):
        s = i * size
        e = s + size + 1 if i < chunks - 1 else len(theta)
        ax.plot(X_full[s:e], Y_full[s:e], Z_full[s:e], color='lightgray', linewidth=50, alpha=0.3, zorder=1)
    return list(zip(X_full, Y_full, Z_full))


# --- Chunked Segment ---
def draw_segment(ax, p1, p2, color='blue', chunks=100):
    t = np.linspace(0, 1, 150)
    x = p1[0] + t * (p2[0] - p1[0])
    y = p1[1] + t * (p2[1] - p1[1])
    # Lines hover slightly outside (r_offset=0.05)
    X, Y, Z = rect_to_torus(x, y)

    size = len(X) // chunks
    for i in range(chunks):
        s = i * size
        e = s + size + 1 if i < chunks - 1 else len(X)
        ax.plot(X[s:e], Y[s:e], Z[s:e], color=color, linewidth=4, zorder=5)
    return list(zip(X, Y, Z))


# --- OBJ Export Function ---
def export_to_obj(filename, all_line_paths):
    """
    Exports a list of line paths (each a list of xyz tuples) to OBJ format.
    """
    with open(filename, 'w') as f:
        f.write("# Toroidal K4,4 Export\n")
        v_offset = 1
        for path in all_line_paths:
            for v in path:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            # Connect the vertices as a line
            indices = [str(i) for i in range(v_offset, v_offset + len(path))]
            f.write(f"l {' '.join(indices)}\n")
            v_offset += len(path)
    print(f"Successfully exported to {filename}")


colors = ['red', 'green', 'blue', 'purple']
# --- Materials and Color definitions ---
# Create 16 colors for the edges by blending existing ones
edge_colors = colors * 4
edge_colors.insert(0, 'lightgray')  # Add spine color at index 0


def create_mtl_file(mtl_filename, color_list):
    """Generates an MTL file with material definitions for each color."""
    with open(mtl_filename, 'w') as f:
        f.write("# Toroidal Material Library\n\n")

        # Define 17 materials (1 spine + 16 edges)
        for i, color_name in enumerate(color_list):
            mat_name = f"Mat_{i}"
            f.write(f"newmtl {mat_name}\n")

            # Map the Python color names to RGB for the diffuse color (Kd)
            from matplotlib.colors import to_rgb
            rgb = to_rgb(color_name)

            # Kd is diffuse color (red, green, blue).
            # Ka is ambient color. Ks is specular (shine).
            f.write(f"Kd {rgb[0]:.3f} {rgb[1]:.3f} {rgb[2]:.3f}\n")
            f.write(f"Ka {rgb[0]:.2f} {rgb[1]:.2f} {rgb[2]:.2f}\n")  # Saturated ambient
            f.write("Ks 0.2 0.2 0.2\n")  # Some shine
            f.write("Ns 10\n")  # Specular exponent
            f.write("d 1.0\n")  # Fully opaque
            f.write("illum 2\n\n")
    print(f"Generated material library: {mtl_filename}")


def generate_tube(path, radius=0.05, sides=8):
    """Turns a 3D path into a tube mesh (vertices and faces)."""
    vertices = []
    faces = []

    for i in range(len(path)):
        p = np.array(path[i])
        # Find the vector pointing forward to the next point
        if i < len(path) - 1:
            forward = np.array(path[i + 1]) - p
        else:
            forward = p - np.array(path[i - 1])

        # Normalize and find perpendicular vectors for the ring
        forward /= np.linalg.norm(forward)
        arbitrary = np.array([0, 1, 0]) if abs(forward[1]) < 0.9 else np.array([1, 0, 0])
        right = np.cross(forward, arbitrary)
        right /= np.linalg.norm(right)
        up = np.cross(forward, right)

        # Create a ring of vertices around the point
        for j in range(sides):
            angle = 2 * np.pi * j / sides
            offset = (np.cos(angle) * right + np.sin(angle) * up) * radius
            vertices.append(p + offset)

        # Connect this ring to the previous ring
        if i > 0:
            start_idx = (i - 1) * sides + 1
            curr_idx = i * sides + 1
            for j in range(sides):
                next_j = (j + 1) % sides
                faces.append((start_idx + j, start_idx + next_j, curr_idx + j))
                faces.append((curr_idx + j, start_idx + next_j, curr_idx + next_j))

    return vertices, faces


def export_mesh_to_obj(filename, export_paths, tube_radius=0.04):
    """Exports each path in export_paths as a separate named object."""
    v_offset = 1  # OBJ indices are 1-based

    with open(filename, 'w') as f:
        f.write("# K4,4 Toroidal Mesh Export - Multi-Object Version\n")

        for i, path in enumerate(export_paths):
            # 1. Label the Object
            if i == 0:
                f.write("o Torus_Spine\n")
                r = 1  # Thicker spine
            else:
                f.write(f"o Edge_{i}\n")
                r = tube_radius

            # 2. Generate the geometry for this specific path
            verts, faces = generate_tube(path, radius=r, sides=8)

            # 3. Write Vertices
            for v in verts:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")

            # 4. Write Faces using the global index offset
            for face in faces:
                f.write(f"f {face[0] + v_offset - 1} {face[1] + v_offset - 1} {face[2] + v_offset - 1}\n")

            # Update the global vertex offset for the next object
            v_offset += len(verts)

    print(f"Mesh exported to {filename}. Open it in Blender to see separate objects!")


def export_multimat_obj(obj_filename, mtl_filename, export_paths, tube_radius=0.04):
    """
    Exports each path as a separate object with its own distinct material.
    """
    with open(obj_filename, 'w') as f:
        f.write(f"# K4,4 Toroidal Mesh Export\n")
        f.write(f"mtllib {mtl_filename}\n\n")  # Tells the OBJ to look for the MTL

        v_offset = 1  # Global vertex offset

        for i, path in enumerate(export_paths):
            # 1. Define the Object
            if i == 0:
                f.write(f"o Torus_Spine\n")
                f.write(f"usemtl Mat_0\n")  # Spine uses first color (lightgray)
                r = 1  # Thicker spine
            else:
                f.write(f"o Edge_{i}\n")
                f.write(f"usemtl Mat_{i}\n")  # Edge uses color from matched edge_colors
                r = tube_radius

            # 2. Generate the tube mesh geometry
            # This generates relative faces, so we must shift them!
            verts, faces = generate_tube(path, radius=r, sides=8)

            # 3. Write Vertices
            for v in verts:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")

            # 4. Write Faces, shifting the indices by v_offset
            for face in faces:
                # v_offset - 1 because face indices from generate_tube are 1-based
                f.write(f"f {face[0] + v_offset - 1} {face[1] + v_offset - 1} {face[2] + v_offset - 1}\n")

            # 5. Update the global vertex offset for the next object
            v_offset += len(verts)

    print(f"Mesh exported to {obj_filename} with separate materials!")

# --- Segments ---
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

# --- Main Plotting ---
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection='3d')

# Track all paths for OBJ export
export_paths = []

# Draw Spine
spine_path = draw_torus_spine(ax)
export_paths.append(spine_path)

# Draw Segments
for i, seg in enumerate(segments):
    path = draw_segment(ax, seg[0], seg[1], color=colors[i % len(colors)])
    export_paths.append(path)

# Final Styling
ax.set_box_aspect([4, 4, 1])
ax.axis('off')
plt.show()

# --- Export Trigger ---
export_to_obj("torus_graph.obj", export_paths)
export_mesh_to_obj("torus_mesh.obj", export_paths)
export_multimat_obj("torus_multimat.obj", "torus_multimat.mtl", export_paths)
create_mtl_file("torus_multimat.mtl", edge_colors)