from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicBoolean
from bpy.props import BoolProperty


@node_type
class LogicNodeCharacterInfo(LogicNodeParameterType):
    bl_idname = "NLActionGetCharacterInfo"
    bl_label = "Get Physics Info"
    nl_module = 'uplogic.nodes.parameters'
    bl_description = "Current Status of a 'Character' physics type object"
    nl_class = "ULCharacterInfo"

    local: BoolProperty(default=True)

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_output(NodeSocketLogicInteger, 'Max Jumps', 'MAX_JUMPS')
        self.add_output(NodeSocketLogicInteger, 'Current Jump Count', 'CUR_JUMP')
        self.add_output(NodeSocketLogicVectorXYZ, 'Gravity', 'GRAVITY')
        self.add_output(NodeSocketLogicVectorXYZ, 'Walk Direction', 'WALKDIR')
        self.add_output(NodeSocketLogicBoolean, 'On Ground', 'ON_GROUND')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "local", text='Local')

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object"]

    def get_attributes(self):
        return [("local", self.local)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["MAX_JUMPS", "CUR_JUMP", "GRAVITY", 'WALKDIR', 'ON_GROUND']
