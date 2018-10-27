#!/usr/bin/env python

# --- Imports

from samr.geometry import CartesianGeometry
from samr.mesh import Box
from samr.mesh import Mesh


# --- Main program

# Construct domain
num_dimensions = 2

lower = [1] * num_dimensions
upper = [5] * num_dimensions
domain = [Box(lower, upper)]

# Construct geometry
x_lower = [0] * num_dimensions
x_upper = [1] * num_dimensions
geometry = CartesianGeometry(x_lower, x_upper)

# Construct mesh
mesh = Mesh(domain, geometry)

# Create variables
u = mesh.create_variable()

print(mesh)
print(u)

data_via_mesh = u.data(mesh)
print("u.data(mesh)")
print(data_via_mesh)

data_via_block = u.data(mesh.block)
print("u.data(mesh.block)")
print(data_via_block)
print("u.data(mesh) == u.data(mesh.block):",
      data_via_mesh is data_via_block)

data_from_mesh = mesh.data(u)
print("mesh.data(u)")
print(data_from_mesh)
print("u.data(mesh) == mesh.data(u):",
      data_via_mesh is data_from_mesh)
