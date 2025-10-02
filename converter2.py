import meshio
import numpy as np

# --- Configuration ---
# The original file exported from Ansys
INPUT_MSH_FILE = "input.msh" 
# The name of the final, RTMsim-compatible file
OUTPUT_BDF_FILE = "output_for_RTMsim.bdf"

# --- Main Script ---

print(f"Step 1: Reading mesh data from '{INPUT_MSH_FILE}'...")
try:
    mesh = meshio.read(INPUT_MSH_FILE)
except Exception as e:
    print(f"\nFATAL ERROR: Could not read the input file '{INPUT_MSH_FILE}'.")
    exit()

points = mesh.points
triangle_cells = None
try:
    for cell_block in mesh.cells:
        if cell_block.type == "triangle":
            triangle_cells = cell_block.data
            break
    if triangle_cells is None:
        raise ValueError("No triangle cells were found in the mesh object.")
except (ValueError, IndexError) as e:
    print(f"\nFATAL ERROR: Could not find triangle element data within '{INPUT_MSH_FILE}'.")
    exit()

num_points = len(points)
num_elements = len(triangle_cells)

print(f"Step 2: Successfully read {num_points} nodes and {num_elements} triangle elements.")
print(f"Step 3: Writing to RTMsim-compatible BDF file: '{OUTPUT_BDF_FILE}'...")

try:
    with open(OUTPUT_BDF_FILE, 'w') as f:
        f.write("$ Generated for RTMsim with classic small-field GRID format\n")
        f.write("BEGIN BULK\n")
        
        prop_id = 1
        mat_id = 1
        # We're going to write some assumed values here, RTMsim ignores this, I think.
        f.write(f"{'PSHELL':<8}{prop_id:>8}{mat_id:>8}{1.0:>8.1f}\n")
        f.write(f"{'MAT1':<8}{mat_id:>8}{2.1e+5:>8.1e}{'':>8}{0.3:>8.1f}\n")

        # Write nodes using the small-field GRID format (8-character columns)
        # This is the most compatible format for older or simpler parsers.
        for i, point in enumerate(points):
            node_id = i + 1
            x, y, z = point
            # Format: GRID, ID, CP, X, Y, Z
            # The {:>8.4f} specifier ensures a fixed-width float representation.
            f.write(f"{'GRID':<8}{node_id:>8}{'':>8}{x:>8.4f}{y:>8.4f}{z:>8.4f}\n")

        # The element format remains the same, as it was already correct.
        for i, cell in enumerate(triangle_cells):
            element_id = i + 1
            node1 = cell[0] + 1
            node2 = cell[1] + 1
            node3 = cell[2] + 1
            f.write(f"{'CTRIA3':<8}{element_id:>8}{prop_id:>8}{node1:>8}{node2:>8}{node3:>8}\n")

        f.write("ENDDATA\n")

    print("\n--- CONVERSION COMPLETE ---")
    print(f"The RTMsim-compatible file is: '{OUTPUT_BDF_FILE}'")

except Exception as e:
    print(f"\nFATAL ERROR: An unexpected error occurred while writing the BDF file.")
    print(f"Error details: {e}")