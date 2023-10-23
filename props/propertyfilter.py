import bpy
from .property import propgroup


_filter_prop_types = [
    ("TREES", "Logic Trees", "Show only applied Logic Trees"),
    ("FLOAT", "Floats", "Show only Float Properties"),
    ("INT", "Integers", "Show only Int Properties"),
    ("BOOL", "Booleans", "Show only Boolean Properties"),
    ("STRING", "Strings", "Show only String Properties"),
    ("TIMER", "Timers", "Show only Timer Properties"),
    ("NAME", 'Filter By Name', 'Search for a Property')
]


@propgroup
class LogicNodesPropertyFilter(bpy.types.PropertyGroup):
    do_filter: bpy.props.BoolProperty(
        name='Filter',
        description='Filter properties by type or name'
    )
    filter_by: bpy.props.EnumProperty(
        items=_filter_prop_types,
        default='NAME'
    )
    filter_name: bpy.props.StringProperty(name='Property Name')
    show_hidden: bpy.props.BoolProperty(
        name='Show Hidden',
        default=True,
        description='Show properties that start with "."'
    )
    show_trees: bpy.props.BoolProperty(
        name='Show Trees',
        default=True,
        description='Show applied logic trees'
    )
    collapse_trees: bpy.props.BoolProperty(
        name='Collapse Trees',
        default=True,
        description='Compress Logic Tree Properties to an immutable form (recommended)'
    )