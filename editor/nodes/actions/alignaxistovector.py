from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicAxisSigned
from ...sockets import NodeSocketLogicFloatFactor
from bpy.props import BoolProperty


@node_type
class LogicNodeAlignAxisToVector(LogicNodeActionType):
    bl_idname = "NLActionAlignAxisToVector"
    bl_label = "Align Axis to Vector"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULAlignAxisToVector"

    local: BoolProperty(default=False, name='Local')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector")
        self.add_input(NodeSocketLogicAxisSigned, "Axis")
        self.add_input(NodeSocketLogicFloatFactor, "Factor", {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "local")

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "game_object", "vector", "axis", 'factor']

    def get_attributes(self):
        return [("local", self.local)]
