import typing
from ..generator.bl_text_buffer import BLTextBuffer
from ..generator.file_text_buffer import FileTextBuffer
from ..generator.tree_code_generator import TreeCodeGenerator
from ..editor.nodetree import LogicNodeTree
from ..utilities import ERROR_MESSAGES
from ..utilities import WARNING_MESSAGES
from ..utilities import warn
from .operator import operator
from bpy.types import Context, Operator
from bpy.props import BoolProperty
import bpy
from ..utilities import check_uplogic_module
from ..generator.tree_code_generator import generate_logic_node_code


@operator
class LOGIC_NODES_OT_generate_code(Operator):
    bl_idname = "logic_nodes.generate_code"
    bl_label = "Generate Logic Nodes Code"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Force generation of code, needed only after updating or if encountering issues"
    uplogic_installed: BoolProperty()

    @classmethod
    def poll(cls, context):
        return True

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

    def execute(self, context: Context):
        generate_logic_node_code()
        return {'FINISHED'}

    # def generate(self):
        


    def invoke(self, context, event):

        # import pkg_resources
        # installed_packages = [p.key for p in pkg_resources.working_set]
        # self.uplogic_installed = 'uplogic' in installed_packages
        # if not self.uplogic_installed:
        #     bpy.context.window_manager.popup_menu(uplogic_message, title="Uplogic module missing", icon='INFO')
        check_uplogic_module()
            # context.window_manager.modal_handler_add(self)
            # return {'RUNNING_MODAL'}
        # for package in installed_packages:
        #     print(f"{package.key}=={package.version}")
        generate_logic_node_code()
        return {'FINISHED'}

    # def modal(self, context, event):
    #     def installer_msg(self, context):
    #         self.layout.label(text="Everything is ready to go!")
        
        # if not self.uplogic_installed:
            # bpy.ops.logic_nodes.install_uplogic()
            # bpy.context.window_manager.popup_menu(installer_msg, title="Finished", icon='CHECKBOX_HLT')
        # self.generate()
        return {"FINISHED"}