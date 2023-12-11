from .operator import operator
from .operator import reload_texts
from bpy.types import Operator


@operator
class LOGIC_NODES_OT_reload_texts(Operator):
    bl_idname = "logic_nodes.reload_texts"
    bl_label = "Reload Scripts"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Reload all externally saved scripts"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        reload_texts()
        return {'FINISHED'}