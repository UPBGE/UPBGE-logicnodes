from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicListItem
from ...sockets import NodeSocketLogicParameter
from bpy.types import Context, UILayout
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


@node_type
class LogicNodeListNew(LogicNodeParameterType):
    bl_idname = "NLInitNewList"
    bl_label = "List From Items"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULListFromItems"
    deprecated = True
    deprecation_message = 'Node was replaced by newer version, please re-add'

    def init(self, context):
        self.add_input(NodeSocketLogicListItem, 'Item')
        self.add_input(NodeSocketLogicListItem, 'Item')
        self.add_output(NodeSocketLogicList, 'List')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        op = layout.operator('logic_nodes.add_socket')
        op.socket_type = 'NLListItemSocket'

    def set_new_input_name(self):
        self.inputs[-1].name = 'Item'

    def setup(
        self,
        cell_varname,
        uids
    ):
        items = ''
        for socket in self.inputs:
            field_value = None
            if socket.linked_valid:
                field_value = self.get_linked_value(
                    socket,
                    uids
                )
            else:
                field_value = socket.get_default_value()
            items += f'{field_value}, '
        items = items[:-2]
        return f'        {cell_varname}.items = [{items}]\n'

    def get_output_names(self):
        return ['LIST']


# @node_type
# class LogicNodeListFromItems(LogicNodeParameterType):
#     bl_idname = "LogicNodeListFromItems"
#     bl_label = "List From Items"
#     nl_module = 'uplogic.nodes.parameters'
#     nl_class = "ListFromItemsNode"

#     def init(self, context):
#         self.add_input(NodeSocketLogicParameter, 'Items', 'items', settings={'link_limit': 0}, multi=True)
#         self.add_output(NodeSocketLogicList, 'List', 'LIST')
#         LogicNodeParameterType.init(self, context)


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
class LogicNodeListFromItems(LogicNodeParameterType):
    bl_idname = "LogicNodeListFromItems"
    bl_label = "List From Items"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ListFromItemsNode"

    def update_draw(self, context=None):
        mode = int(self.mode)
        ipts = self.inputs
        opts = self.outputs
        ipts[0].enabled = opts[0].enabled = mode in [0]
        ipts[1].enabled = opts[1].enabled = mode in [1]
        ipts[2].enabled = opts[2].enabled = mode in [2]
        ipts[3].enabled = opts[3].enabled = mode in [3]
        ipts[4].enabled = opts[4].enabled = mode in [4]
        ipts[5].enabled = opts[5].enabled = mode in [5]
        ipts[6].enabled = opts[6].enabled = mode in [6]
        ipts[7].enabled = opts[7].enabled = mode in [7]
        ipts[8].enabled = opts[8].enabled = mode in [8]
        ipts[9].enabled = opts[9].enabled = mode in [9]
        ipts[10].enabled = opts[10].enabled = mode in [10]
        ipts[11].enabled = opts[11].enabled = mode in [11]
        ipts[12].enabled = opts[12].enabled = mode in [12]
        ipts[13].enabled = opts[13].enabled = mode in [13]
        ipts[14].enabled = opts[14].enabled = mode in [14]

    mode: EnumProperty(items=modes, name='Type', update=update_draw, default='0')
    
    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'mode')

    def init(self, context):
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

        self.add_output(NodeSocketLogicValue, "Values", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicFloat, "Floats", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicInteger, "Integers", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicString, "Strings", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicBoolean, "Booleans", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicVector, "Vectors", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicColorRGBA, "Colors", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicList, "Lists", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicDictionary, "Dictionaries", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicDatablock, "Datablocks", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicObject, "Objects", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicCollection, "Collections", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicCondition, "Conditions", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicPython, "Instances", 'LIST', shape='SQUARE')
        self.add_output(NodeSocketLogicUI, "Widgets", 'LIST', shape='SQUARE')

        LogicNodeParameterType.init(self, context)
