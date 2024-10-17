import bpy
from .property import propgroup


@propgroup
class LogicNodesFmodParameters(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name', default='')
    users: bpy.props.IntProperty()
