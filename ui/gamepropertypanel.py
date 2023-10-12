import bpy
from ..utilities import NLPREFIX
from ..utilities import preferences
from ..editor.nodetree import LogicNodeTree
from .interface import ui_panel


class LOGIC_NODES_PT_game_property_panel(bpy.types.Panel):
    bl_label = "Game Properties (Advanced)"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"

    @classmethod
    def poll(cls, context):
        return False

    def draw_tree_prop(self, prop, index, box, show_movers):
        col = box.column()
        name = prop.name.split('__')[-1]
        text = 'Logic Tree'
        opts_row = col.row()
        opts_row.label(text=text)
        val_row = col.row()
        val_row.label(text=name)
        val_row.prop(prop, 'value', text='Start')
        if show_movers:
            self.add_movers(index, opts_row)
        opts_row.operator(
                'logic_nodes.unapply_logic_tree',
                text="",
                icon="X"
        ).tree_name = name

    def add_movers(self, index, layout):
        movers = layout.row(align=True)
        move_up = movers.operator(
            'logic_nodes.move_game_property',
            text='',
            icon='TRIA_UP'
        )
        move_up.direction = 'UP'
        move_down = movers.operator(
            'logic_nodes.move_game_property',
            text='',
            icon='TRIA_DOWN'
        )
        move_down.direction = 'DOWN'
        move_down.index = move_up.index = index

    def draw(self, context):
        layout = self.layout
        column = layout.column()
        obj = bpy.context.object
        column.operator(
            'logic_nodes.add_game_property',
            text="Add Game Property",
            icon='PLUS'
        )
        options = column.row()
        filter = preferences().prop_filter
        show_hidden = filter.show_hidden
        collapse_trees = filter.collapse_trees
        do_filter = filter.do_filter
        prop_type = filter.filter_by
        prop_name = filter.filter_name
        show_trees = filter.show_trees

        hide_icon = 'HIDE_OFF' if show_hidden else 'HIDE_ON'
        collapse_icon = 'LOCKED' if collapse_trees else 'UNLOCKED'
        options.prop(
            filter,
            'do_filter',
            icon='FILTER',
            text=''
        )
        options.prop(
            filter,
            'show_hidden',
            icon=hide_icon,
            text=''
        )
        options.prop(
            filter,
            'show_trees',
            icon='OUTLINER',
            text=''
        )
        options.prop(
            filter,
            'collapse_trees',
            icon=collapse_icon,
            text=''
        )

        if do_filter:
            column.prop(filter, 'filter_by', text='')
        if prop_type == 'NAME' and do_filter:
            column.prop(
                filter,
                'filter_name',
                text='',
                icon='VIEWZOOM'
            )
        if not obj:
            return

        show_movers = show_hidden and show_trees and not do_filter

        props = [prop for prop in obj.game.properties]
        for prop in obj.game.properties:
            if not show_hidden and prop.name.startswith('.'):
                continue
            is_tree = prop.name.startswith(NLPREFIX)
            if is_tree and not show_trees:
                continue
            has_name = prop_name in prop.name
            if do_filter:
                if prop_type == 'NAME':
                    if not has_name:
                        continue
                elif prop_type == 'TREES':
                    if not is_tree:
                        continue
                elif prop.type != prop_type or is_tree:
                    continue
            index = props.index(prop)
            # column.separator()
            box = column.box()
            if is_tree and collapse_trees:
                self.draw_tree_prop(prop, index, box, show_movers)
                continue
            entry = box.column()
            row_title = entry.row()
            row_title.prop(prop, 'name', text='')
            row_title.prop(prop, 'show_debug', text='', icon='INFO')
            if show_movers:
                self.add_movers(index, row_title)
            remove = row_title.operator(
                'logic_nodes.remove_game_property',
                text='',
                icon='X'
            )
            remove.index = index
            row_info = entry.split()
            row_info.prop(prop, 'type', text='')
            row_info.prop(prop, 'value', text='')
        context.region.tag_redraw()


# @ui_panel
class LOGIC_NODES_PT_game_property_panel_nodes(LOGIC_NODES_PT_game_property_panel):
    bl_label = "Game Properties"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Dashboard"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        if not ob:
            return False
        sel = ob.select_get()
        enabled = (context.space_data.tree_type == LogicNodeTree.bl_idname)
        return sel and ob.name and enabled


@ui_panel
class LOGIC_NODES_PT_game_property_panel_3d(LOGIC_NODES_PT_game_property_panel):
    bl_label = "Game Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        if not ob:
            return False
        sel = ob.select_get()
        return sel and ob.name


# @ui_panel
class LOGIC_NODES_PT_game_property_panel_properties(LOGIC_NODES_PT_game_property_panel):
    bl_label = "Game Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "game"
    name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        if not ob:
            return False
        sel = ob.select_get()
        return sel and ob.name