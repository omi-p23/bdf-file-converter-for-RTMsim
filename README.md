This code converts .msh files to .bdf files. It does this by extracting model info using meshio and writes a .bdf file from scratch.
Be warned, this will round down the precision of your nodes from 16 to 8!

It requires meshio, python, and numpy to work.
