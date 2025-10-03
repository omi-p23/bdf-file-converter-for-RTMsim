# Mesh to RTMsim BDF Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

A Python script for converting 3D mesh files into the Nastran Bulk Data File (`.bdf`) format, with specific formatting required for compatibility with the RTMsim software.

## Background

Standard mesh conversion utilities often produce BDF files that are incompatible with the parsers found in specialized academic software like RTMsim. 

The primary incompatibilities addressed in this script are:
1.  **Node Coordinate Format:** The script generates node data using the fixed-width, small-field `GRID` card format, as opposed to the large-field `GRID*` format which is not always supported.
2.  **Missing Property Definitions:** The BDF standard requires that all elements are associated with a property card. This script automatically generates the necessary placeholder `PSHELL` and `MAT1` cards to ensure the file is valid.
3.  **Proper Formatting:** The script manually constructs each line of the BDF file to enforce the column-based alignment required by the Nastran format, preventing parsing errors.

## Functionality

-   **Input:** Accepts any mesh file format readable by the `meshio` library (e.g., `.msh`, `.stl`, `.obj`, `.inp`, `.vtk`).
-   **Processing:** The script parses the input file and extracts the node coordinates and the element connectivity data for triangular elements (`CTRIA3`) only. All other element types are ignored.
-   **Output:** A `.bdf` file containing the triangular mesh geometry, formatted for use in RTMsim.

## Requirements

-   Python 3.6 or newer
-   `meshio` and `numpy` Python libraries.

Install the required libraries via pip:
```bash
pip install meshio numpy
```

## Usage

The script is executed from the command line, with the input file and output file paths provided as arguments.

**Syntax:**
```bash
python convert_to_rtmsim.py <input_file> <output_file.bdf>
```

**Example:**
```bash
python convert_to_rtmsim.py blade_profile.msh blade_profile.bdf
```

## Implementation Details

1.  **File Input:** The `meshio` library is used to read the source mesh file. `meshio` automatically detects the file format and parses the geometric data.
2.  **Data Extraction:** The script accesses the `points` and `cells` attributes of the `meshio` object. It iterates through the cell blocks to find the data corresponding to the `triangle` element type.
3.  **File Output:** The script writes the output `.bdf` file manually on a line-by-line basis. Python's string formatting capabilities are used to ensure that all data fields are right-aligned within their designated 8-character columns, as specified by the small-field Nastran BDF standard.

## License

MIT License.
