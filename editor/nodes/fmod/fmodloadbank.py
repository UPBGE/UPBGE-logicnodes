from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFilePath
from bpy.props import BoolProperty


@node_type
class LogicNodeFModLoadBank(LogicNodeActionType):
    bl_idname = "LogicNodeFModLoadBank"
    bl_label = "Load Bank"
    bl_description = 'Load a .bank file created by FMOD'
    nl_module = 'uplogic.nodes.fmod'
    nl_class = "FModLoadBankNode"
    
    load_master: BoolProperty(name='Load Master.bank', description='Load "Master.bank" from the same directory')
    load_strings: BoolProperty(name='+ strings.bank', description='Load "Master.strings.bank" from the same directory')

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'load_master')
        if self.load_master:
            layout.prop(self, 'load_strings')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicFilePath, "Path", 'path')
        self.add_output(NodeSocketLogicCondition, "Done", 'OUT')
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [
            ('load_master', self.load_master),
            ('load_strings', self.load_strings)
        ]
