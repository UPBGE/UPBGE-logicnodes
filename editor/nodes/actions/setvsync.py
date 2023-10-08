from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...enum_types import _enum_vsync_modes
from bpy.props import EnumProperty


@node_type
class LogicNodeSetVSync(LogicNodeActionType):
    bl_idname = "NLActionSetVSync"
    bl_label = "Set VSync"
    nl_category = 'Render'
    nl_module = 'actions'
    vsync_mode: EnumProperty(items=_enum_vsync_modes)
    nl_class = "ULSetVSync"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'vsync_mode', text='')

    def get_output_names(self):
        return ["OUT"]

    def get_attributes(self):
        return [('vsync_mode', self.vsync_mode)]

    def get_input_names(self):
        return ["condition"]
