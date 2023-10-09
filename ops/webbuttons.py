from .operator import operator
from bpy.types import Operator
import webbrowser


@operator
class LOGIC_NODES_OT_open_donate(Operator):
    bl_idname = "logic_nodes.open_donate"
    bl_label = "Support this Project"
    bl_description = "Please consider supporting this Add-On"

    def execute(self, context):
        webbrowser.open('https://www.patreon.com/iza_zed')
        return {"FINISHED"}


@operator
class LOGIC_NODES_OT_open_upbge_manual(Operator):
    bl_idname = "logic_nodes.open_upbge_manual"
    bl_label = "Manual"
    bl_description = "Manual on engine and node usage"

    def execute(self, context):
        webbrowser.open('https://upbge.org/#/documentation/docs/latest/manual/manual/logic_nodes/index.html')
        return {"FINISHED"}


@operator
class LOGIC_NODES_OT_open_upbge_docs(Operator):
    bl_idname = "logic_nodes.open_upbge_docs"
    bl_label = "Engine API"
    bl_description = "UPBGE API Documentation"

    def execute(self, context):
        webbrowser.open('https://upbge.org/#/documentation/docs/latest/api/index.html')
        return {"FINISHED"}


@operator
class LOGIC_NODES_OT_open_github(Operator):
    bl_idname = "logic_nodes.open_github"
    bl_label = "GitHub"
    bl_description = "Get involved with development"

    def execute(self, context):
        webbrowser.open('https://github.com/IzaZed/Uchronian-Logic-UPBGE-Logic-Nodes/issues')
        return {"FINISHED"}