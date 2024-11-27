import bpy
from .interface import ui_panel
from ..editor.nodetree import LogicNodeTree


@ui_panel
class LOGIC_NODES_PT_administration(bpy.types.Panel):
    bl_label = "Administration"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == LogicNodeTree.bl_idname)
        return enabled

    def draw(self, context):
        layout = self.layout
        apply = layout.box()
        apply_col = apply.column()
        apply_col.scale_y = 1.4
        apply_col.operator(
            'logic_nodes.apply_logic_tree',
            text="Apply To Selected",
            icon='PREFERENCES'
        ).owner = "BGE_PT_LogicPanel"
        # cmtree = context.scene.custom_mainloop_tree
        # is_scene_tree = cmtree is context.space_data.edit_tree
        # apply_col.operator(
        #     'logic_nodes.custom_mainloop_tree',
        #     text='Unset Scene Logic' if is_scene_tree else 'Set as Scene Logic',
        #     icon='REMOVE' if is_scene_tree else 'PLAY'
        # )
        code = layout.box()
        code.operator(
            'logic_nodes.generate_code',
            text="Force Compile",
            icon='FILE_SCRIPT'
        )