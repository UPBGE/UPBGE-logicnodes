from .operator import operator
from bpy.types import Operator
from bpy.props import StringProperty


@operator
class LOGIC_NODES_OT_get_owner(Operator):
    bl_idname = "logic_nodes.get_owner"
    bl_label = "Select"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Select the object this tree is applied to"
    applied_object: StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = context.view_layer.objects.get(self.applied_object)
        context.view_layer.objects.active = obj
        obj.select_set(True)
        return {'FINISHED'}