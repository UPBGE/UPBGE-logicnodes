from .operator import operator
from bpy.types import Operator


@operator
class LOGIC_NODES_OT_remove_global_category(Operator):
    bl_idname = "logic_nodes.remove_global_category"
    bl_label = "Remove Global Category"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove a global value category"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        scene.nl_global_categories.remove(scene.nl_global_cat_selected)
        if scene.nl_global_cat_selected > len(scene.nl_global_categories) - 1:
            scene.nl_global_cat_selected = len(scene.nl_global_categories) - 1
        return {'FINISHED'}
