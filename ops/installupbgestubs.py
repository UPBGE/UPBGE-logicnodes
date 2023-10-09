from ..utilities import notify
from ..utilities import error
from ..utilities import success
from .operator import operator
from bpy.types import Operator
import os, sys


@operator
class LOGIC_NODES_OT_install_upbge_stubs(Operator):
    bl_idname = "logic_nodes.install_upbge_stubs"
    bl_label = "Install or Update BGE Stub Module"
    bl_description = (
        'Downloads the latest version of the upbge-stubs module to support autocomplet in your IDE.'
        'NOTE: This may take a few seconds and requires internet connection.'
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        notify('Installing bge stub module...')
        try:
            os.system(f'"{sys.executable}" -m ensurepip')
            os.system(f'"{sys.executable}" -m pip install upbge-stubs==0.3.1.26.dev1705922753')
            success('Installed.')
        except Exception as e:
            error('Install failed. Error:')
            error(e)
        return {"FINISHED"}