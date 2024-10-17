from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloat


@node_type
class LogicNodeClamp(LogicNodeParameterType):
    bl_idname = "NLClampValueNode"
    bl_label = "Clamp"
    bl_description = 'Constrain a value in between two others'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULClamp"

    def init(self, context):
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_input(NodeSocketLogicVectorXY, "", 'range', {'enabled': False})
        self.add_input(NodeSocketLogicFloat, "Min", 'min_value')
        self.add_input(NodeSocketLogicFloat, "Max", 'max_value', {'default_value': 1.0})
        self.add_output(NodeSocketLogicFloat, "Value", 'OUT')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["value", "range", "min_value", "max_value"]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['OUT']
