from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeGetMasterFolder(LogicNodeParameterType):
    bl_idname = "LogicNodeGetMasterFolder"
    bl_label = "Get Master Folder"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "GetMasterFolderNode"

    def init(self, context):
        self.add_input(NodeSocketLogicString, 'Name', 'name')
        self.add_output(NodeSocketLogicString, "Path", 'PATH')
        LogicNodeParameterType.init(self, context)
