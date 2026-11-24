# PyVista CFD Data

## Dataset

This project uses the PyVista electronics cooling dataset.

It contains two files:

- `structure.vtp`: Surface mesh representing the cooling structure.
- `air.vtu`: Volume mesh representing the surrounding air region.

What I did:

1. Loaded both mesh files using PyVista.
2. Inspected mesh information, including points, cells, bounds, and arrays.
3. Examined point data and cell data.
4. Visualized temperature and velocity magnitude.
5. Created slice and clip views.
6. Converted cell data to point data.
7. Extracted coordinates and field arrays using NumPy.
8. Saved and reloaded the extracted data using `.npz`.

What surprised me:

The air mesh contains a velocity field with three components, giving it a shape of `(610176, 3)`, while most other fields are one-dimensional arrays.

The structure mesh also contains temperature and wall heat flux in both point data and cell data.