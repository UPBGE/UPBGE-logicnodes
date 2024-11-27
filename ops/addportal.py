from .operator import operator
from bpy.types import Operator
from bpy.props import StringProperty
from bpy.props import EnumProperty
from bpy.props import BoolProperty
from ..editor.enum_types import _socket_types
import bpy


@operator
class LOGIC_NODES_OT_add_portal_in(Operator):
    bl_idname = "logic_nodes.add_portal_in"
    bl_label = "New Portal"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Create a new portal"
    
    def get_portals(self, context, edit_text):
        if edit_text != '' and edit_text not in [portal.name for portal in bpy.context.scene.nl_portals]:
            yield edit_text
        for portal in context.scene.nl_portals:
            yield (portal.name, 'PLUS')

    portal_name: StringProperty(default='Portal', name='Portal Name')#, search=get_portals)
    mode: EnumProperty(default='1', name='Socket Type', items=_socket_types)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.node.add_node(use_transform=True, type='LogicNodeSetPortal')
        node = context.space_data.edit_tree.nodes[-1]
        node.portal = self.portal_name
        node.nl_label = self.portal_name
        node.mode = self.mode
        node.hide = True
        bpy.ops.node.translate_attach("INVOKE_DEFAULT")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


@operator
class LOGIC_NODES_OT_add_portal_out(Operator):
    bl_idname = "logic_nodes.add_portal_out"
    bl_label = "New Portal"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Create a new portal"
    
    def get_portals(self, context, edit_text):
        if edit_text != '' and edit_text not in [portal.name for portal in bpy.context.scene.nl_portals]:
            yield edit_text
        for portal in context.scene.nl_portals:
            yield (portal.name, 'PLUS')

    portal_name: StringProperty(default='', name='Portal Name', search=get_portals)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.node.add_node(use_transform=True, type='LogicNodeGetPortal')
        node = context.space_data.edit_tree.nodes[-1]

        node.portal = self.portal_name
        node.nl_label = self.portal_name
        node.hide = True
        bpy.ops.node.translate_attach("INVOKE_DEFAULT")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)