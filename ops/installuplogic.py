from typing import Set, Optional
from ..utilities import notify
from ..utilities import preferences
from ..utilities import error
from ..utilities import success
from .operator import operator
from bpy.types import Context, Operator
from importlib.metadata import version as pkg_version, PackageNotFoundError
import os, sys
import bpy
import importlib.util


def get_uplogic_installed_version() -> Optional[str]:
    """Return installed uplogic version or None if not installed."""
    if importlib.util.find_spec("uplogic") is None:
        return None
    if pkg_version is None:
        return "unknown"  # present but cannot read version
    try:
        return pkg_version("uplogic")
    except PackageNotFoundError:
        return "unknown"


def requirement_satisfied(installed: Optional[str], required: Optional[str]) -> bool:
    """if required is 'latest' or empty, any installed is fine; else exact match."""
    if not installed:
        return False
    if not required or required == "latest":
        return True
    return installed == required


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

    def need_install(self) -> bool:
        """Return True if installation/update is needed (minimal logic)."""
        req = preferences().uplogic_version if hasattr(preferences(), "uplogic_version") else "latest"
        installed = get_uplogic_installed_version()
        if requirement_satisfied(installed, req):
            success(f'Uplogic already installed (v{installed}).')
            return False
        return True

    def execute(self, context: Context) -> Set[str]:
        if not self.need_install():
            return {"FINISHED"}

        notify('Installing uplogic module...')
        if not bpy.app.online_access:
            error('Online Access is needed to install uplogic.')
            bpy.context.window_manager.popup_menu(failed_message, title="Error", icon='INFO')
            return {"FINISHED"}
        context.window_manager.modal_handler_add(self)
        bpy.context.window_manager.popup_menu(working_message, title="Uplogic module missing", icon='INFO')
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        # Mirror execute for minimal diff
        return self.execute(context)

    def modal(self, context, event):
        try:
            os.system(f'"{sys.executable}" -m ensurepip')
            version = preferences().uplogic_version
            if version == 'latest' or not version:
                os.system(f'"{sys.executable}" -m pip install uplogic --upgrade')
            else:
                os.system(f'"{sys.executable}" -m pip install uplogic=={version}')
            success('Installed.')
            bpy.context.window_manager.popup_menu(finished_message, title="Success", icon='INFO')
        except Exception as e:
            error('Install failed. Error:')
            error(e)
            bpy.context.window_manager.popup_menu(failed_message, title="Error", icon='INFO')
        return {"FINISHED"}
