from ..utilities import error
from ..utilities import success
from ..utilities import compute_initial_status_of_tree
from ..utilities import set_network_initial_status_key
from ..utilities import make_valid_name
from ..utilities import check_uplogic_module
from ..utilities import add_tree_to_active_objects
# from ..generator.tree_code_generator import TreeCodeGenerator
from .operator import operator
from bpy.types import Operator
from bpy.props import StringProperty
from ..editor.nodetree import LogicNodeTree
import bpy


@operator
class LOGIC_NODES_OT_apply_logic_tree(Operator):
    bl_idname = "logic_nodes.apply_logic_tree"
    bl_label = "Apply Logic"
    bl_description = "Apply the current tree to the selected objects."
    bl_options = {'REGISTER', 'UNDO'}

    owner: StringProperty()

    @classmethod
    def poll(cls, context):
        if not hasattr(context.space_data, 'edit_tree'):
            return False
        tree = context.space_data.edit_tree
        if not tree:
            return False
        if not (tree.bl_idname == LogicNodeTree.bl_idname):
            return False
        scene = context.scene
        for ob in scene.objects:
            if ob.select_get():
                return True
        return False

    def execute(self, context):
        # current_scene = context.scene
        check_uplogic_module()
        tree = context.space_data.edit_tree
        # active_object = context.object
        # if not active_object:
        #     error('Missing active object, aborting...')
        #     return {'FINISHED'}
        # tree.use_fake_user = True
        # selected_objects = [
        #     ob for ob in current_scene.objects if ob.select_get()
        # ]
        # initial_status = compute_initial_status_of_tree(
        #     tree.name, selected_objects
        # )
        # try:
        #     TreeCodeGenerator().write_code_for_tree(tree)
        # except Exception as e:
        #     error(f"Couldn't compile tree {tree.name}!")
        #     print(e)
        # initial_status = True if initial_status is None else False
        # for obj in selected_objects:
        #     tree_name = make_valid_name(tree.name)
        #     module = f'nl_{tree_name.lower()}'
        #     name = f'{module}.{tree_name}'
        #     comps = [c.module for c in obj.game.components]
        #     if obj.name in bpy.context.view_layer.objects:
        #         bpy.context.view_layer.objects.active = obj
        #     else:
        #         error(f'Object {obj.name} not in view layer, please check for references. Skipping...')
        #         continue
        #     if module not in comps:
        #         bpy.ops.logic.python_component_register(component_name=name)
        #         success(
        #             "Applied tree {} to object {}.".format(
        #                 tree.name,
        #                 obj.name
        #             )
        #         )
        #     else:
        #         success(
        #             "Tree {} already applied to object {}. Updating status.".format(
        #                 tree.name,
        #                 obj.name
        #             )
        #         )
        #     tree_collection = obj.logic_trees
        #     contains = False
        #     for t in tree_collection:
        #         if t.tree_name == tree.name:
        #             contains = True
        #             break
        #     if not contains:
        #         new_entry = tree_collection.add()
        #         new_entry.tree_name = tree.name
        #         new_entry.tree = tree
        #         # this will set both new_entry.tree_initial_status and add a
        #         # game property that makes the status usable at runtime
        #         set_network_initial_status_key(
        #             obj, tree_name, initial_status
        #         )
        # bpy.context.view_layer.objects.active = active_object
        add_tree_to_active_objects(tree)
        return {'FINISHED'}