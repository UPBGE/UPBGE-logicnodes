from .operator import operator
from bpy.types import Operator


@operator
class LOGIC_NODES_OT_add_global_category(Operator):
    bl_idname = "logic_nodes.add_global_category"
    bl_label = "Add Global Category"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a global value category"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        cats = scene.nl_global_categories
        cat = cats.add()
        cat.name = 'category'
        scene.nl_global_cat_selected = len(scene.nl_global_categories) - 1

        return {'FINISHED'}