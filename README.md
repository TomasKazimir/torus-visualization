## Torus visualisation

This project includes a simple python script that visualises the complete bipartite graph K_{4,4}
on the surface of a torus. It uses the `matplotlib` library to create a 3D plot of the torus and the edges of the graph.

While this is easy to run and visualise, `matplotlib` struggles with proper rednering of the edges and the torus
in the correct order, leading to a somewhat messy visualisation.

For a more usable and interactive visualisation, the script also generates .obj files:
- `torus_graph.obj`: Simple lines representing the edges of the graph.
- `torus_mesh.obj`: A mesh representation of the torus and the edges of the graph,
allowing for better rendering and interaction in 3D modeling software.
- `torus_multimat.obj`: A more complex .obj file that includes multiple materials
for different parts of the graph and torus, enhancing the visual distinction between them.
- `torus_multimat.mtl`: The material file associated with `torus_multimat.obj`, defining the colors and properties
of the materials used in the .obj file.

## Usage
The project is built using `uv` and can be run with the following command:

```bash
uv run plotting.py
```

This will execute the `plotting.py` script,
which opens a matplotlib window with the visualisation of the torus and the graph.
After the visualisation is closed, the .obj files will be generated in the current directory.

## Dependencies
- `matplotlib`: For visualising the torus and the graph in a 3D plot.
- `numpy`: For numerical operations and generating the torus and graph data.
- `uv`: For managing the project and running the script.
- 3D modeling software (optional): To view and interact with the generated .obj files,
you can use software like Blender or any other 3D model viewer that supports .obj files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
