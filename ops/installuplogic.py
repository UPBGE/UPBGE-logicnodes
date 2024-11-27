from typing import Set
from ..utilities import notify
from ..utilities import preferences
from ..utilities import error
from ..utilities import success
from .operator import operator
from bpy.types import Context, Operator
import os, sys
import bpy


def working_message(self, context):
    self.layout.label(text='Downloading, this may take a few moments...')


def finished_message(self, context):
    self.layout.label(text='Download complete, ready to go.', icon='CHECKBOX_HLT')


def failed_message(self, context):
    self.layout.label(text='Download failed. Please check connection and try again.', icon='CANCEL')


@operator
class LOGIC_NODES_OT_install_uplogic(Operator):
    bl_idname = "logic_nodes.install_uplogic"
    bl_label = "Install or Update Uplogic Module"
    bl_description = (
        'Downloads the latest version of the uplogic module required for '
        'running logic nodes.\n\n'
        'NOTE: This may take a few seconds and requires internet connection.'
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: Context) -> Set[str]:
        notify('Installing uplogic module...')
        if not bpy.app.online_access:
            error('Online Access is needed to install uplogic.')
            bpy.context.window_manager.popup_menu(failed_message, title="Error", icon='INFO')
            return {"FINISHED"}
        context.window_manager.modal_handler_add(self)
        bpy.context.window_manager.popup_menu(working_message, title="Uplogic module missing", icon='INFO')
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        notify('Installing uplogic module...')
        if not bpy.app.online_access:
            error('Online Access is needed to install uplogic.')
            bpy.context.window_manager.popup_menu(failed_message, title="Error", icon='INFO')
            return {"FINISHED"}
        context.window_manager.modal_handler_add(self)
        bpy.context.window_manager.popup_menu(working_message, title="Uplogic module missing", icon='INFO')
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        try:
            os.system(f'"{sys.executable}" -m ensurepip')
            version = preferences().uplogic_version
            if version == 'latest':
                os.system(f'"{sys.executable}" -m pip install uplogic --upgrade')
            else:
                os.system(f'"{sys.executable}" -m pip install uplogic=={preferences().uplogic_version}')
            success('Installed.')
            bpy.context.window_manager.popup_menu(finished_message, title="Success", icon='INFO')
        except Exception as e:
            error('Install failed. Error:')
            error(e)
            bpy.context.window_manager.popup_menu(failed_message, title="Error", icon='INFO')
        return {"FINISHED"}