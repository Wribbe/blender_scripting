import bpy
import sys
import os
import pytoml

#import pudb; pudb.set_trace()

from bpy import context
from math import sin, cos, radians

with open("dims.toml") as fp:
    dims = pytoml.load(fp)

def get_scale(key):
    return list(dims[key].values())[:3]

def get_object(name):
    return objects()[name]

def scale(obj, vector):
    obj.scale = vector

def values(key):
    return list(dims[key].values())

def objects():
    return bpy.data.objects

def add_cube(location=[0,0,0], dim=[1,1,1], layers=[True]+19*[False]):
    prev_objects = set(objects())
    bpy.ops.mesh.primitive_cube_add(location=location, layers=layers)
    obj = list(set(objects()).difference(prev_objects))[0]
    scale(obj, dim)
    return obj

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

#intersecting_cube = add_cube()
#intersecting_cube.scale = (2,2,2)


bpy.context.scene.render.filepath = os.path.join(
    DIR_IMG,
    "{}.png".format(OUTPUT_NAME)
)

# Modify table top solid.
key_table = list(dims.keys())[0]
table_top = get_object('Cube')
scale(table_top, get_scale(key_table))
# Punch hole in solid top.
border = dims[key_table]["border"]
table_hole = add_cube(dim=[v-border for v in get_scale(key_table)])
table_hole.scale.z = 1
#bpy.data.objects.active = table_hole

for obj in bpy.data.objects:
    obj.select = False

#table_top.select = True
#table_hole.select = True
#bpy.ops.object.mode_set(mode='OBJECT')
#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.object.modifier_add(type='BOOLEAN')

#print(dir(bpy.context.selected_objects[0]))
#bpy.ops.object.mode_set('EDIT')
#bpy.ops.object.delete()
#bpy.ops.mesh.intersect_boolean()

#bool_one = table_top.modifiers.new(type="BOOLEAN", name="bool 1")
#bool_one.object = table_hole
#bool_one.operation = 'DIFFERENCE'
#
#bpy.ops.object.modifier_apply(apply_as='DATA', modifier="bool 1")
#table_hole.hide = True

target = table_top
otherobject = table_hole

target.select = True
bpy.context.scene.objects.active = target

bpy.ops.object.modifier_add(type='BOOLEAN')
mod = target.modifiers
mod[0].name = "SubEmUp"
mod[0].object = otherobject
mod[0].operation = 'DIFFERENCE'

bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod[0].name)
otherobject.hide_render = True

bpy.ops.render.render(write_still = True)
print(sys.argv)
print(border)
print([v-border for v in values(key_table)])
print(dir(otherobject))
