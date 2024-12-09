import bpy
from .property import check_double_prop
from .property import propgroup


_enum_value_types = [
    ("0", "Float", "A Float value"),
    ("1", "String", "A String"),
    ("2", "Integer", "An Integer value"),
    ("3", "Bool", "A True/False value"),
    ("17", "File Path", 'Choose a file path'),
    None,
    ('4', 'Vector', ''),
    ('5', 'Color', ''),
    ('6', 'Color Alpha', ''),
    None,
    ('7', 'Object', ''),
    ('8', 'Collection', ''),
    ('9', 'Material', ''),
    ('10', 'Mesh', ''),
    ('11', 'Node Tree', ''),
    ('12', 'Action', ''),
    None,
    ('13', 'Text', ''),
    ('14', 'Sound', ''),
    ('15', 'Image', ''),
    ('16', 'Font', '')
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

    vec_val: bpy.props.FloatVectorProperty(name='Vector')
    color_val: bpy.props.FloatVectorProperty(name='Color', subtype='COLOR_GAMMA', min=0.0, max=1.0)
    color_alpha_val: bpy.props.FloatVectorProperty(name='Color', subtype='COLOR_GAMMA', size=4, min=0.0, max=1.0)

    obj_val: bpy.props.PointerProperty(name='Object', type=bpy.types.Object)
    collection_val: bpy.props.PointerProperty(name='Collection', type=bpy.types.Collection)
    material_val: bpy.props.PointerProperty(name='Material', type=bpy.types.Material)
    mesh_val: bpy.props.PointerProperty(name='Mesh', type=bpy.types.Mesh)
    node_tree_val: bpy.props.PointerProperty(name='Node Tree', type=bpy.types.NodeTree)
    action_val: bpy.props.PointerProperty(name='Action', type=bpy.types.Action)

    text_val: bpy.props.PointerProperty(name='Text', type=bpy.types.Text)
    sound_val: bpy.props.PointerProperty(name='Sound', type=bpy.types.Sound)
    image_val: bpy.props.PointerProperty(name='Image', type=bpy.types.Image)
    font_val: bpy.props.PointerProperty(name='Font', type=bpy.types.VectorFont)

    persistent: bpy.props.BoolProperty(name='Persistent')