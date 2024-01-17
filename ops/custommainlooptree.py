from .operator import operator
from .custommainloop import make_custom_mainloop
from bpy.types import Operator
from ..editor.nodetree import LogicNodeTree
import bpy


@operator
class LOGIC_NODES_OT_custom_mainloop_tree(Operator):
    bl_idname = "logic_nodes.custom_mainloop_tree"
    bl_label = "Use a logic tree for scene logic."
    bl_description = ('Use a custom Mainloop for this scene')
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not hasattr(context.space_data, 'edit_tree'):
            return False
        tree = context.space_data.edit_tree
        if not tree:
            return False
        if not (tree.bl_idname == LogicNodeTree.bl_idname):
            return False
        elif tree:
            return True
        return False

    def execute(self, context):
        scene = context.scene
        if not scene.get('__main__') and not scene.get('custom_mainloop_tree'):
            make_custom_mainloop(scene)
        tree = context.space_data.edit_tree
        if scene.custom_mainloop_tree is tree:
            scene.custom_mainloop_tree = None
        else:
            scene.custom_mainloop_tree = tree
        return {"FINISHED"}