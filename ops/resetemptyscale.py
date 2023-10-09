from .operator import operator
from bpy.types import Operator


@operator
class LOGIC_NODES_OT_reset_empty_scale(Operator):
    bl_idname = "logic_nodes.reset_empty_scale"
    bl_label = "Set Reverb Volume"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Reset the volume scale"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob and ob.name

    def execute(self, context):
        from mathutils import Vector
        context.active_object.scale = Vector((1, 1, 1))
        context.active_object.empty_display_type = 'CUBE'
        return {"FINISHED"}