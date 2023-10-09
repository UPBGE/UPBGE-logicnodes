from ..utilities import warn
from ..utilities import error
from .operator import operator
from bpy.types import Operator
from bpy.props import StringProperty


@operator
class LOGIC_NODES_OT_key_selector(Operator):
    bl_idname = "logic_nodes.key_selector"
    bl_label = "Press a Key"
    bl_options = {'REGISTER', 'UNDO'}

    keycode: StringProperty()

    def __init__(self):
        self.socket = None
        self.node = None
        self._old_val = None

    def __del__(self):
        pass

    def execute(self, context):
        return {'FINISHED'}

    def cleanup(self, context):
        if self.socket.value == "Press a key...":
            self.socket.value = ""
        self.socket = None
        self.node = None
        try:
            context.region.tag_redraw()
        except Exception:
            warn("Couldn't redraw panel, code updated.")

    def modal(self, context, event):
        if event.value == "PRESS":
            if (
                event.type == "LEFTMOUSE" or
                event.type == "MIDDLEMOUSE" or
                event.type == "RIGHTMOUSE"
            ):
                self.socket.value = self._old_val
                return {'CANCELLED'}
            else:
                value = event.type
                self.socket.value = value
                self.cleanup(context)
                return {'FINISHED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self.socket = context.socket
        self.node = context.node

        if (not self.socket) and (not self.node):
            error("No socket or Node")
            return {'FINISHED'}

        self._old_val = self.socket.value
        self.socket.value = "Press a key..."
        try:
            context.region.tag_redraw()
        except Exception:
            warn("Couldn't redraw panel, code updated.")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}