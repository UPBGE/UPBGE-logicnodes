import bpy
from .property import propgroup


@propgroup
class LogicNodesFmodParameter(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name', default='')
    users: bpy.props.IntProperty()
