from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicAxis
from ...sockets import NodeSocketLogicAxisSigned


@node_type
class LogicNodeRotateTo(LogicNodeActionType):
    bl_idname = "NLActionRotateTo"
    bl_label = "Rotate To"
    bl_description = 'Rotate an object to a point along an axis'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULActionRotateTo"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'moving_object')
        self.add_input(NodeSocketLogicVectorXYZ, "Target", 'target_point')
        self.add_input(NodeSocketLogicFloatFactor, "Factor", 'speed', {'default_value': 1.0})
        self.add_input(NodeSocketLogicAxis, "Rot Axis", 'rot_axis', {'default_value': '2'})
        self.add_input(NodeSocketLogicAxisSigned, "Front", 'front_axis', {'default_value': '1'})
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "moving_object",
            "target_point",
            "speed",
            "rot_axis",
            "front_axis"
        ]