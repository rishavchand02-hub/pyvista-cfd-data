import pyvista as pv
from pyvista import examples
import numpy as np
import os

print("Current directory:", os.getcwd())


output_folder = os.path.join(os.path.dirname(__file__), "outputs")

os.makedirs(output_folder, exist_ok=True)
# Get file paths
files = examples.download_electronics_cooling(load=False)

# Read both files
structure = pv.read(files[0])
air = pv.read(files[1])

# Inspect structure
print("STRUCTURE")
print("Type:", type(structure))
print("Points:", structure.n_points)
print("Cells:", structure.n_cells)
print("Bounds:", structure.bounds)
print("Arrays:", structure.array_names)

print("\nAIR")
print("Type:", type(air))
print("Points:", air.n_points)
print("Cells:", air.n_cells)
print("Bounds:", air.bounds)
print("Arrays:", air.array_names)


def inspect_mesh(mesh, name):

    print("\n==========", name, "==========")

    
    for array_name in mesh.point_data:

        data = mesh.point_data[array_name]

        print("\nName:", array_name)
        print("Location: Point Data")
        print("Shape:", data.shape)
        print("Minimum:", data.min())
        print("Maximum:", data.max())

    
    for array_name in mesh.cell_data:

        data = mesh.cell_data[array_name]

        print("\nName:", array_name)
        print("Location: Cell Data")
        print("Shape:", data.shape)
        print("Minimum:", data.min())
        print("Maximum:", data.max())


inspect_mesh(structure, "STRUCTURE")
inspect_mesh(air, "AIR")

velocity = air["U"]

velocity_magnitude = np.linalg.norm(velocity, axis=1)

air["U_magnitude"] = velocity_magnitude



plotter = pv.Plotter(off_screen=True)

plotter.add_mesh(
    air,
    scalars="T",
    show_edges=False
)

plotter.show(
    screenshot=os.path.join(output_folder, "temperature.png")
)



plotter = pv.Plotter(off_screen=True)

plotter.add_mesh(
    air,
    scalars="U_magnitude",
    show_edges=False
)

plotter.show(
    screenshot=os.path.join(output_folder, "velocity.png")
)

# Slice through the middle of the mesh
sliced_mesh = air.slice(normal="z", origin=air.center)

plotter = pv.Plotter(off_screen=True)

plotter.add_mesh(
    sliced_mesh,
    scalars="T"
)

plotter.show(
    screenshot=os.path.join(output_folder, "temperature_slice.png")
)
# Clip half of the mesh
clipped_mesh = air.clip(normal="x", origin=air.center)

plotter = pv.Plotter(off_screen=True)

plotter.add_mesh(
    clipped_mesh,
    scalars="U_magnitude"
)

plotter.show(
    screenshot=os.path.join(output_folder, "velocity_clip.png")
)


sliced = air.slice(normal="z", origin=air.center)

sliced.plot(
    scalars="T",
    screenshot=os.path.join(output_folder, "slice.png")
)


clipped = air.clip(normal="x", origin=air.center)

clipped.plot(
    scalars="T",
    screenshot=os.path.join(output_folder, "clip.png")
)


converted = structure.cell_data_to_point_data()


# Original cell temperature
plotter = pv.Plotter(off_screen=True)

plotter.add_mesh(
    structure,
    scalars="T",
    preference="cell"
)

plotter.show(
    screenshot=os.path.join(output_folder, "cell_temperature.png")
)


# Converted point temperature
plotter = pv.Plotter(off_screen=True)

plotter.add_mesh(
    converted,
    scalars="T",
    preference="point"
)

plotter.show(
    screenshot=os.path.join(output_folder, "converted_temperature.png")
)
# Load mesh and extract arrays
def load_case(path):

    mesh = pv.read(path)

    data = {}

    # Extract coordinates
    data["coords"] = mesh.points

    # Extract point data
    for name in mesh.point_data:
        data[name] = mesh.point_data[name]

    # Extract cell data
    for name in mesh.cell_data:
        data[name + "_cell"] = mesh.cell_data[name]

    return data
# Load air simulation data
air_data = load_case(files[1])

print("\nExtracted arrays:")

for name, array in air_data.items():
    print(name, array.shape)

# Save extracted data
np.savez(
    os.path.join(output_folder, "air_data.npz"),
    **air_data
)

# Load saved data
loaded_data = np.load(
    os.path.join(output_folder, "air_data.npz")
)

# Check shapes
print("\nChecking saved data:")

for name in air_data:
    print(
        name,
        "Original:", air_data[name].shape,
        "Loaded:", loaded_data[name].shape
    )    