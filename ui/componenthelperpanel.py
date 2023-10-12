import bpy
from .interface import ui_panel


@ui_panel
class LOGIC_NODES_PT_component_helper(bpy.types.Panel):
    bl_label = "Component Helper"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "game"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob and ob.name

    def draw(self, context):
        layout = self.layout
        layout.operator('logic_nodes.reload_components', text='Reload Components', icon='RECOVER_LAST')
        row = layout.row()
        row.label(text=f'Add Component To {context.active_object.name}:')
        row = layout.row(align=True)
        row.prop(bpy.context.scene, 'componenthelper', text='')
        row.operator("logic_nodes.add_component", text='Select Component', icon="PLUS")
