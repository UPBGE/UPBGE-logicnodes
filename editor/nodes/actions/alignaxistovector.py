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
    bl_description = "Point a specific object axis towards a position"

    local: BoolProperty(default=False, name='Local')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", "condition")
        self.add_input(NodeSocketLogicObject, "Object", "game_object")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector", "vector")
        self.add_input(NodeSocketLogicAxisSigned, "Axis", "axis")
        self.add_input(NodeSocketLogicFloatFactor, "Factor", 'factor', {'default_value': 1.0})
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "local")

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "game_object",
            "vector",
            "axis",
            'factor'
        ]

    def get_attributes(self):
        return [("local", self.local)]
