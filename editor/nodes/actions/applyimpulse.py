from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from bpy.props import BoolProperty


@node_type
class LogicNodeApplyImpulse(LogicNodeActionType):
    bl_idname = "NLActionApplyImpulse"
    bl_label = "Apply Impulse"
    nl_category = "Objects"
    nl_subcat = 'Transformation'
    nl_module = 'actions'

    deprecated = True
    deprecation_message = 'Replaced by "Apply Transform" Node.'
    local: BoolProperty(default=False, name='Local')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicObject, 'Object')
        self.add_input(NodeSocketLogicVectorXYZ, 'Point')
        self.add_input(NodeSocketLogicVectorXYZ, 'Direction')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def draw_buttons(self, context, layout):
        layout.prop(self, "local")

    nl_class = "ULApplyImpulse"

    def get_input_names(self):
        return ["condition", "game_object", "point", 'impulse']

    def get_attributes(self):
        return [("local", self.local)]
