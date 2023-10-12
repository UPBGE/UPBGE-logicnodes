import bpy
from .property import check_double_prop
from .property import propgroup


_enum_value_types = [
    ("FLOAT", "Float", "A Float value"),
    ("STRING", "String", "A String"),
    ("INTEGER", "Integer", "An Integer value"),
    ("BOOLEAN", "Bool", "A True/False value"),
    ("FILE_PATH", "File Path", 'Choose a file path')
]


@propgroup
class LogicNodesGlobalValue(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name', default='prop', update=check_double_prop)
    value_type: bpy.props.EnumProperty(items=_enum_value_types, name='Value Types')
    string_val: bpy.props.StringProperty(name='String')
    float_val: bpy.props.FloatProperty(name='Floating Point')
    int_val: bpy.props.IntProperty(name='Integer')
    bool_val: bpy.props.BoolProperty(name='Boolean')
    filepath_val: bpy.props.StringProperty(name='File Path', subtype='FILE_PATH')
    persistent: bpy.props.BoolProperty(name='Persistent')