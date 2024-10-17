from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from bpy.props import BoolProperty


@node_type
class LogicNodeApplyMovement(LogicNodeActionType):
    bl_idname = "NLActionApplyLocation"
    bl_label = "Apply Movement"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULApplyMovement"
    bl_description = "Linearly modify an object's position"

    deprecated = True
    deprecation_message = 'Replaced by "Apply Transform" Node.'

    local: BoolProperty(default=True)

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicVectorXYZ, "Vector", 'vector')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "local")

    def get_input_names(self):
        return ["condition", "game_object", "movement"]

    def get_attributes(self):
        return [("local", self.local)]
