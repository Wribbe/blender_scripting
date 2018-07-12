import bpy
import sys
import os
import pytoml

#import pudb; pudb.set_trace()

from bpy import context
from math import sin, cos, radians

with open("dims.toml") as fp:
    dims = pytoml.load(fp)

def objects():
    return bpy.data.objects

def add_cube(location=[0,0,0], dim=[1,1,1], layers=[True]+19*[False]):
    prev_objects = set(objects())
    bpy.ops.mesh.primitive_cube_add(layers=layers)
    return list(set(objects()).difference(prev_objects))[0]

layers = [False]*20
layers[0] = True

cursor = context.scene.cursor_location

radius = 5
anglesInRadians = [radians(degree) for degree in range(0, 360, 65)]

DIR_IMG=""
OUTPUT_NAME=""

for arg in sys.argv:
    if "img_dir" in arg:
        DIR_IMG = arg.split('=')[-1]
    elif ".py" in arg:
        OUTPUT_NAME = arg.split('.py')[0]


#for theta in anglesInRadians:
#    x = cursor.x + radius * cos(theta)
#    y = cursor.y + radius * sin(theta)
#    z = cursor.z
#    add_cube(location=(x, y, z), layers=layers)

intersecting_cube = add_cube()
intersecting_cube.scale = (2,2,2)


bpy.context.scene.render.filepath = os.path.join(
    DIR_IMG,
    "{}.png".format(OUTPUT_NAME)
)

# Modify one cube.
bpy.data.objects['Cube'].scale = (3, 2, 1)

bpy.ops.render.render(write_still = True)
print(sys.argv)
print(dims)
