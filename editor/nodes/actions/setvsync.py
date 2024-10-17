from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...enum_types import _enum_vsync_modes
from bpy.props import EnumProperty


@node_type
class LogicNodeSetVSync(LogicNodeActionType):
    bl_idname = "NLActionSetVSync"
    bl_label = "Set VSync"
    bl_description = 'Set the state of vertical synchronization'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetVSync"

    vsync_mode: EnumProperty(items=_enum_vsync_modes, name='Mode')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition', 'condition')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'vsync_mode', text='')

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    def get_attributes(self):
        return [('vsync_mode', self.vsync_mode)]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition"]
