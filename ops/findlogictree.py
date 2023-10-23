from ..utilities import error
from .operator import operator
from bpy.types import Operator
from bpy.props import StringProperty
from ..editor.nodetree import LogicNodeTree
import bpy


@operator
class LOGIC_NODES_OT_find_logic_tree(Operator):
    bl_idname = "logic_nodes.find_logic_tree"
    bl_label = "Edit"
    bl_description = "Edit"
    tree_name: StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        assert self.tree_name is not None
        assert len(self.tree_name) > 0
        blt_groups = [
            g for g in bpy.data.node_groups if (
                g.name == self.tree_name
            ) and (
                g.bl_idname == LogicNodeTree.bl_idname
            )
        ]
        if len(blt_groups) != 1:
            error("Something went wrong here...")
        for t in blt_groups:
            context.space_data.node_tree = t
        return {'FINISHED'}