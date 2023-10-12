import bpy
from .globalvalue import LogicNodesGlobalValue
from .property import propgroup
from .property import check_double_cat


@propgroup
class LogicNodesGlobalCategory(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name', default='category', update=check_double_cat)
    content: bpy.props.CollectionProperty(type=LogicNodesGlobalValue)
    selected: bpy.props.IntProperty(name='Value')