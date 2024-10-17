from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVector
from ...sockets import NodeSocketLogicDatablock
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicUI
from ...sockets import NodeSocketLogicCollection
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicDictionary
from bpy.props import EnumProperty


modes = [
    ('', 'Type', ''),
    ('0', 'Generic', ''),
    None,
    ('1', 'Float', ''),
    ('2', 'Integer', ''),
    ('3', 'String', ''),
    ('4', 'Boolean', ''),
    None,
    ('5', 'Vector', ''),
    ('6', 'Color', ''),
    ('7', 'List', ''),
    ('8', 'Dictionary', ''),
    ('', '', ''),
    ('9', 'Datablock', ''),
    ('10', 'Object', ''),
    ('11', 'Collection', ''),
    None,
    ('12', 'Condition', ''),
    ('13', 'Python Object Instance', ''),
    ('14', 'UI Widget', '')
]


@node_type
class LogicNodeLoop(LogicNodeParameterType):
    bl_idname = "LogicNodeLoop"
    bl_label = "Loop"
    bl_description = 'Execute the following logic for each item in a list'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "LoopNode"

    def update_draw(self, context=None):
        mode = int(self.mode)
        ipts = self.inputs
        opts = self.outputs
        ipts[1].enabled = opts[1].enabled = mode in [0]
        ipts[2].enabled = opts[2].enabled = mode in [1]
        ipts[3].enabled = opts[3].enabled = mode in [2]
        ipts[4].enabled = opts[4].enabled = mode in [3]
        ipts[5].enabled = opts[5].enabled = mode in [4]
        ipts[6].enabled = opts[6].enabled = mode in [5]
        ipts[7].enabled = opts[7].enabled = mode in [6]
        ipts[8].enabled = opts[8].enabled = mode in [7]
        ipts[9].enabled = opts[9].enabled = mode in [8]
        ipts[10].enabled = opts[10].enabled = mode in [9]
        ipts[11].enabled = opts[11].enabled = mode in [10]
        ipts[12].enabled = opts[12].enabled = mode in [11]
        ipts[13].enabled = opts[13].enabled = mode in [12]
        ipts[14].enabled = opts[14].enabled = mode in [13]
        ipts[15].enabled = opts[15].enabled = mode in [14]

    mode: EnumProperty(items=modes, name='Type', update=update_draw, default='0')
    
    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicValue, "Values", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicFloat, "Floats", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicInteger, "Integers", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicString, "Strings", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicBoolean, "Booleans", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicVector, "Vectors", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicColorRGBA, "Colors", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicList, "Lists", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicDictionary, "Dictionaries", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicDatablock, "Datablocks", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicObject, "Objects", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicCollection, "Collections", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicCondition, "Conditions", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicPython, "Instances", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)
        self.add_input(NodeSocketLogicUI, "Widgets", 'items', shape='SQUARE', settings={'link_limit': 0}, multi=True)

        self.add_output(NodeSocketLogicCondition, "Loop", 'LOOP', shape='SQUARE')
        self.add_output(NodeSocketLogicValue, "Value", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicFloat, "Float", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicInteger, "Integer", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicString, "String", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicBoolean, "Boolean", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicVector, "Vector", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicColorRGBA, "Color", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicList, "List", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicDictionary, "Dictionary", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicDatablock, "Datablock", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicObject, "Object", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicCollection, "Collection", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicCondition, "Condition", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicPython, "Instance", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicUI, "Widget", 'LIST', shape='SQUARE')

        LogicNodeParameterType.init(self, context)


@node_type
class LogicNodeListLoop(LogicNodeParameterType):
    bl_idname = "LogicNodeLoopFromList"
    bl_label = "Loop from List"
    bl_description = 'Execute the following logic for each item in a list'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "LoopNode"

    def update_draw(self, context=None):
        mode = int(self.mode)
        opts = self.outputs
        opts[1].enabled = mode in [0]
        opts[2].enabled = mode in [1]
        opts[3].enabled = mode in [2]
        opts[4].enabled = mode in [3]
        opts[5].enabled = mode in [4]
        opts[6].enabled = mode in [5]
        opts[7].enabled = mode in [6]
        opts[8].enabled = mode in [7]
        opts[9].enabled = mode in [8]
        opts[10].enabled = mode in [9]
        opts[11].enabled = mode in [10]
        opts[12].enabled = mode in [11]
        opts[13].enabled = mode in [12]
        opts[14].enabled = mode in [13]
        opts[15].enabled = mode in [14]

    mode: EnumProperty(items=modes, name='Type', update=update_draw, default='0')
    
    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicList, "List", 'items', shape='SQUARE')

        self.add_output(NodeSocketLogicCondition, "Loop", 'LOOP', shape='SQUARE')
        self.add_output(NodeSocketLogicValue, "Value", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicFloat, "Float", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicInteger, "Integer", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicString, "String", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicBoolean, "Boolean", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicVector, "Vector", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicColorRGBA, "Color", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicList, "List", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicDictionary, "Dictionary", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicDatablock, "Datablock", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicObject, "Object", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicCollection, "Collection", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicCondition, "Condition", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicPython, "Instance", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicUI, "Widget", 'LIST', shape='SQUARE')

        LogicNodeParameterType.init(self, context)
