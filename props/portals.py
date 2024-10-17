import bpy
from .property import propgroup


@propgroup
class LogicNodesPortal(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name', default='')
    users: bpy.props.IntProperty()
    socket_type: bpy.props.IntProperty()
