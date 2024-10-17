from bpy.types import Context, UILayout
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicList
from ..node import LogicNodeParameterType
from ..node import node_type
from bpy.props import EnumProperty


@node_type
class LogicNodeStringOperation(LogicNodeParameterType):
    bl_idname = "LogicNodeStringOperation"
    bl_label = "String Operation"
    bl_description = 'Perform an operation with strings'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "StringOperationNode"
    
    _operator_types = [
        ('0', 'Join', 'Add second string to first one.'),
        ('1', 'Split', 'Split first string at each occurance of second string.'),
        None,
        ('2', 'Contains', 'Check if second string appears in first string one or more times.'),
        ('3', 'Count', 'Count the occurances of second string in first string.'),
        ('4', 'Replace', 'Replace all occurances of second string in first string with third string (Replace B in A with C).'),
        None,
        ('5', 'Starts With', 'Check if first string starts with second string.'),
        ('6', 'Ends With', 'Check if first string ends with second string.'),
        None,
        ('7', 'To Uppercase', 'Change string to use all upper case.'),
        ('8', 'To Lowercase', 'Change string to use all lower case.'),
        None,
        ('9', 'Prepend Zeroes', 'Add zeroes before the string for a specific amount of digits ("10", Length = 4 -> 0010).')
    ]

    def update_draw(self, context=None):
        mode = int(self.operator)

        self.inputs[1].enabled = mode < 7
        self.inputs[2].enabled = mode == 4
        self.inputs[3].enabled = mode == 9

        self.outputs[0].enabled = mode in [0, 4, 7, 8, 9]  # String
        self.outputs[1].enabled = mode == 1  # List
        self.outputs[2].enabled = mode in [2, 5, 6]  # Condition
        self.outputs[3].enabled = mode == 3  # Integer

    operator: EnumProperty(
        items=_operator_types,
        name='Operation',
        description='Choose which type of operation to perform.',
        update=update_draw
    )
    
    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'operator', text='')

    def init(self, context):
        self.add_input(NodeSocketLogicString, "String", 'string_a')
        self.add_input(NodeSocketLogicString, "String", 'string_b')
        self.add_input(NodeSocketLogicString, "String", 'string_c')
        self.add_input(NodeSocketLogicIntegerPositive, "Length", 'zfill_width')
        self.add_output(NodeSocketLogicString, "String", 'RESULT')
        self.add_output(NodeSocketLogicList, "List", 'RESULT')
        self.add_output(NodeSocketLogicCondition, "Result", 'RESULT')
        self.add_output(NodeSocketLogicIntegerPositive, "Count", 'RESULT')
        LogicNodeParameterType.init(self, context)

    def get_attributes(self):
        return [('operator', self.operator)]
