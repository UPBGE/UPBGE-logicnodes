from .operator import operator
from .. import audio
from bpy.types import Operator


@operator
class LOGIC_NODES_OT_audio_system(Operator):
    bl_idname = "logic_nodes.audio_system"
    bl_label = "Start Audio System"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Select the object this tree is applied to"

    @classmethod
    def poll(cls, context):
        return True

    def modal(self, context, event):
        if audio.SYSTEM is None:
            return {'FINISHED'}
        audio.get_audio_system().update()
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if audio.SYSTEM is None:
            audio.get_audio_system()
        else:
            audio.SYSTEM.shutdown()

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}