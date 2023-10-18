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
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULActionRotateTo"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicVectorXYZ, "Target")
        self.add_input(NodeSocketLogicFloatFactor, "Factor", {'default_value': 1.0})
        self.add_input(NodeSocketLogicAxis, "Rot Axis", {'default_value': '2'})
        self.add_input(NodeSocketLogicAxisSigned, "Front", {'default_value': '1'})
        self.add_output(NodeSocketLogicCondition, "Done")
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "moving_object",
            "target_point",
            "speed",
            "rot_axis",
            "front_axis"
        ]