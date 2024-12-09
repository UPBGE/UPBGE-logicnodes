import bpy
from ..props.property import get_global_category
from ..props.property import get_global_value
from .interface import ui_panel


@ui_panel
class LOGIC_NODES_PT_global_values(bpy.types.Panel):
    bl_label = "Global Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'scene'
    bl_category = "Global Values"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        categories = bpy.context.scene.nl_global_categories
        if len(categories) > 0:
            category = get_global_category()
            row = layout.row()
            row.template_list(
                'LOGIC_NODES_UL_global_category',
                '',
                bpy.context.scene,
                'nl_global_categories',
                bpy.context.scene,
                'nl_global_cat_selected',
                rows=3
            )
            opts = row.column(align=True)
            opts.operator(
                'logic_nodes.add_global_category',
                text='',
                icon='PLUS'
            )
            opts.operator(
                'logic_nodes.remove_global_category',
                text='',
                icon='REMOVE'
            )
            # Draw Category Properties
            row = layout.row()
            value = get_global_value()
            row.template_list(
                'LOGIC_NODES_UL_global_value',
                '',
                category,
                'content',
                category,
                'selected',
                rows=3
            )
            opts = row.column()
            adders = opts.column(align=True)
            adders.operator(
                'logic_nodes.add_global_property',
                text='',
                icon='PLUS'
            )
            adders.operator(
                'logic_nodes.remove_global_property',
                text='',
                icon='REMOVE'
            )
            if value:
                # opts.prop(value, 'persistent', text='', icon='RADIOBUT_ON' if value.persistent else 'RADIOBUT_OFF')
                row2 = layout.row()
                row2.prop(value, 'value_type', text='Type')
        else:
            layout.operator(
                'logic_nodes.add_global_category',
                text='Add Global Category',
                icon='PLUS'
            )