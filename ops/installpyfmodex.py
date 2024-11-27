from ..utilities import notify
from ..utilities import preferences
from ..utilities import error
from ..utilities import success
from .operator import operator
from bpy.types import Operator
import bpy
import os, sys


@operator
class LOGIC_NODES_OT_install_pyfmodex(Operator):
    bl_idname = "logic_nodes.install_pyfmodex"
    bl_label = "Install or Update PyFmodEx Module"
    bl_description = (
        'NOTE: This may take a few seconds and requires internet connection.'
    )
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        def installer_msg(self, context):
            self.layout.label(text="Installed pyfmodex successfully")

        notify('Installing pyfmodex module...')
        if not bpy.app.online_access:
            error('Online Access is needed to install pyfmodex.')
            return {"FINISHED"}
        try:
            os.system(f'"{sys.executable}" -m ensurepip')
            os.system(f'"{sys.executable}" -m pip install pyfmodex --upgrade')
            success('Installed.')
            bpy.context.window_manager.popup_menu(installer_msg, title="Success", icon='INFO')
        except Exception as e:
            error('Install failed. Error:')
            error(e)
        return {"FINISHED"}