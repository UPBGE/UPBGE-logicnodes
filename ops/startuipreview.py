from .operator import operator
from .. import audio
from bpy.types import Operator
from ..editor.nodes.node import WIDGETS
import bpy


@operator
class LOGIC_NODES_OT_start_ui_preview(Operator):
    bl_idname = "logic_nodes.start_ui_preview"
    bl_label = "Start UI Preview"
    bl_options = {'REGISTER'}
    bl_description = "Show this canvas and its children. Children are determined by connected 'Widget' sockets, 'Condition' sockets don't matter"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if WIDGETS.get(context.node, None):
            context.node.end_ui_preview()
        else:
            context.node.start_ui_preview()

        return {'FINISHED'}