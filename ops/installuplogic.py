from ..utilities import notify
from ..utilities import preferences
from ..utilities import error
from ..utilities import success
from .operator import operator
from bpy.types import Operator
import os, sys


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

    def execute(self, context):
        notify('Installing uplogic module...')
        try:
            os.system(f'"{sys.executable}" -m ensurepip')
            version = preferences().uplogic_version
            if version == 'latest':
                os.system(f'"{sys.executable}" -m pip install uplogic --upgrade')
            else:
                os.system(f'"{sys.executable}" -m pip install uplogic=={preferences().uplogic_version}')
            success('Installed.')
        except Exception as e:
            error('Install failed. Error:')
            error(e)
        return {"FINISHED"}