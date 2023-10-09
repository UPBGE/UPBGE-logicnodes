from ..generator.bl_text_buffer import BLTextBuffer
from ..generator.file_text_buffer import FileTextBuffer
from ..generator.tree_code_generator import TreeCodeGenerator
from ..ui import LogicNodeTree
from ..utilities import ERROR_MESSAGES
from ..utilities import WARNING_MESSAGES
from ..utilities import warn
from .operator import operator
from bpy.types import Operator
import bpy


@operator
class LOGIC_NODES_OT_generate_code(Operator):
    bl_idname = "logic_nodes.generate_code"
    bl_label = "Generate Logic Nodes Code"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Create the code needed to execute all logic trees"

    @classmethod
    def poll(cls, context):
        return True

    def __init__(self):
        pass

    def _create_external_text_buffer(self, context, buffer_name):
        file_path = bpy.path.abspath("//{}".format(buffer_name))
        return FileTextBuffer(file_path)

    def _create_text_buffer(self, context, buffer_name, external=False):
        if external is True:
            return self._create_external_text_buffer(context, buffer_name)
        blender_text_data_index = bpy.data.texts.find(buffer_name)
        blender_text_data = None
        if blender_text_data_index < 0:
            blender_text_data = bpy.data.texts.new(name=buffer_name)
        else:
            blender_text_data = bpy.data.texts[blender_text_data_index]
        return BLTextBuffer(blender_text_data)

    def execute(self, context):
        global ERROR_MESSAGES
        ERROR_MESSAGES.clear()
        global WARNING_MESSAGES
        WARNING_MESSAGES.clear()

        for tree in bpy.data.node_groups:
            if tree.bl_idname == LogicNodeTree.bl_idname:
                TreeCodeGenerator().write_code_for_tree(tree)
        try:
            context.region.tag_redraw()
        except Exception:
            warn("Couldn't redraw panel, code updated.")
        
        if ERROR_MESSAGES or WARNING_MESSAGES:
            def error_log(self, context):
                self.layout.label(text=f"Warnings, these may or may not be problematic, but it is recommended to resolve these.", icon='CONSOLE')
                self.layout.label(text=f"Concerned nodes have been marked YELLOW.")
                if WARNING_MESSAGES:
                    self.layout.separator()
                for e in WARNING_MESSAGES:
                    self.layout.label(text=f'{e}')
                if ERROR_MESSAGES:
                    self.layout.separator()
                    self.layout.label(text=f"Errors, these have to be resolved for the tree to work.", icon="ERROR")
                    self.layout.label(text=f"Concerned nodes have been marked RED.")
                    self.layout.separator()
                for e in ERROR_MESSAGES:
                    self.layout.label(text=f'{e}')

            bpy.context.window_manager.popup_menu(error_log, title="Something happened during compilation.", icon='INFO')
        return {"FINISHED"}