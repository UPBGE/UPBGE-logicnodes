from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicBoolean
from ....utilities import update_draw
from bpy.props import BoolProperty


@node_type
class LogicNodeCharacterInfo(LogicNodeParameterType):
    bl_idname = "NLActionGetCharacterInfo"
    bl_label = "Get Physics Info"
    nl_category = "Physics"
    nl_subcat = 'Character'
    nl_module = 'parameters'

    local: BoolProperty(default=True, update=update_draw)

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_output(NodeSocketLogicInteger, 'Max Jumps')
        self.add_output(NodeSocketLogicInteger, 'Current Jump Count')
        self.add_output(NodeSocketLogicVectorXYZ, 'Gravity')
        self.add_output(NodeSocketLogicVectorXYZ, 'Walk Direction')
        self.add_output(NodeSocketLogicBoolean, 'On Ground')

    def draw_buttons(self, context, layout):
        layout.prop(self, "local", text='Local')

    def get_netlogic_class_name(self):
        return "ULCharacterInfo"

    def get_input_names(self):
        return ["game_object"]

    def get_attributes(self):
        return [("local", self.local)]

    def get_output_names(self):
        return ["MAX_JUMPS", "CUR_JUMP", "GRAVITY", 'WALKDIR', 'ON_GROUND']
