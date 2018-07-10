import bpy
import sys
import os

from bpy import context
from math import sin, cos, radians

add_cube = bpy.ops.mesh.primitive_cube_add
layers = [False]*20
layers[0] = True

cursor = context.scene.cursor_location

radius = 5
anglesInRadians = [radians(degree) for degree in range(0, 360, 36)]

DIR_IMG=""
OUTPUT_NAME=""

for arg in sys.argv:
    if "img_dir" in arg:
        DIR_IMG = arg.split('=')[-1]
    elif ".py" in arg:
        OUTPUT_NAME = arg.split('.py')[0]


for theta in anglesInRadians:
    x = cursor.x + radius * cos(theta)
    y = cursor.y + radius * sin(theta)
    z = cursor.z
    add_cube(location=(x, y, z), layers=layers)

bpy.context.scene.render.filepath = os.path.join(
    DIR_IMG,
    "{}.png".format(OUTPUT_NAME)
)

bpy.ops.render.render(write_still = True)
print(sys.argv)
