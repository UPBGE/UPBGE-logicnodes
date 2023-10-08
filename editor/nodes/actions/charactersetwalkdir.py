from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from bpy.props import BoolProperty


@node_type
class LogicNodeCharacterSetWalkDir(LogicNodeActionType):
    bl_idname = "NLActionSetCharacterWalkDir"
    bl_label = "Walk"
    nl_module = 'actions'

    local: BoolProperty(default=True, name='Local')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicVectorXYZ, "Vector")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "local")

    nl_class = "ULSetCharacterWalkDir"

    def get_input_names(self):
        return ["condition", "game_object", 'walkDir']

    def get_attributes(self):
        return [("local", self.local)]
