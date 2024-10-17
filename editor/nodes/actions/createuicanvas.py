from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeUIType
from ..node import WIDGETS
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicUI
from bpy.props import BoolProperty
import bpy



@node_type
class LogicNodeCreateUICanvas(LogicNodeUIType):
    bl_idname = "LogicNodeCreateUICanvas"
    bl_label = "Create Canvas"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULCreateUICanvas"
    bl_description = 'Create a new canvas. This is the root of other widgets'
    
    def get_ui_class(self):
        from uplogic.ui.preview import Canvas
        return Canvas

    def update_draw(self, context=None):
        self.inputs[0].enabled = not self.on_init

    on_init: BoolProperty(name='On Init', update=update_draw, default=True)

    def free(self) -> None:
        self.end_ui_preview()

    def start_ui_preview(self):
        super().start_ui_preview()
        bpy.app.handlers.game_pre.append(self.end_ui_preview)
        for area in bpy.context.window.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        region.tag_redraw()

    def end_ui_preview(self, cam=None, other=None):
        while self.end_ui_preview in bpy.app.handlers.game_pre:
            bpy.app.handlers.game_pre.remove(self.end_ui_preview)
        if WIDGETS.get(self, None) is None:
            return
        WIDGETS[self].unregister()
        del WIDGETS[self]
        for area in bpy.context.window.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        region.tag_redraw()

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        self.add_output(NodeSocketLogicUI, "Canvas", 'CANVAS')
        LogicNodeUIType.init(self, context)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.operator('logic_nodes.start_ui_preview', icon='IMAGE_PLANE', text='End Preview' if WIDGETS.get(self, None) else 'Start Preview')
        layout.prop(self, 'on_init')

    def get_attributes(self):
        return [('on_init', self.on_init)]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT", 'CANVAS']

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition"]
