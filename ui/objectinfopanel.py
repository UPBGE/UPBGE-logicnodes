import bpy
from ..editor.nodetree import LogicNodeTree
from .interface import ui_panel


@ui_panel
class LOGIC_NODES_PT_object_info_panel(bpy.types.Panel):
    bl_label = "Object Trees"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        if not ob:
            return False
        sel = ob.select_get()
        return sel and ob.name and (context.space_data.tree_type == LogicNodeTree.bl_idname)

    def get_combined_status_of_tree_items(self, tree_item_list):
        last = None
        for e in tree_item_list:
            initial_status = e.tree_initial_status
            if last is None:
                last = initial_status
            elif last != initial_status:
                return None
                # None means undefined, mixed,
                # some are enabled, some are disabled
        return last

    def draw(self, context):
        layout = self.layout
        selected_objects = [
            ob for ob in context.scene.objects if ob.select_get()
        ] if not bpy.app.version < (2, 80, 0) else [
            ob for ob in context.scene.objects if ob.select
        ]
        active_tree_items = {}
        title = None
        if context.object:
            box_over = layout.box()
            title = box_over.row()
        for ob in selected_objects:
            for e in ob.logic_trees:
                data = active_tree_items.get(e.tree_name)
                if data is None:
                    data = []
                    active_tree_items[e.tree_name] = data
                data.append(e)
        tree_count = len(active_tree_items.keys())
        if title and context.object:
            title.label(text="Trees applied to {}: {}".format(context.object.name, tree_count))
        for name in active_tree_items:
            box = box_over.box()
            status = self.get_combined_status_of_tree_items(
                active_tree_items[name]
            )
            status_icon = "CHECKBOX_DEHLT"
            if status is None:
                status_icon = "QUESTION"
                status = False
                # For mixed states, apply means "set it to enabled"
            elif status is True:
                status_icon = "CHECKBOX_HLT"
            col = box.column()
            row = col.row(align=False)
            row.label(text=name)
            row.operator(
                'logic_nodes.unapply_logic_tree',
                text="",
                icon="X"
            ).tree_name = name
            data = col.row(align=False)
            data.operator(
                'logic_nodes.find_logic_tree',
                text="Edit",
                icon="NODETREE"
            ).tree_name = name