from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicDictionary

@node_type
class LogicNodeSendOSC(LogicNodeActionType):
    bl_idname = "LogicNodeSendOSC"
    bl_label = "Send OSC Message"
    bl_description = "Send OSC messages to a given address"
    bl_width_default = 180
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSendOSC"
    
    def init(self, context):
        #Inputs
        self.add_input(NodeSocketLogicCondition, "Condition", "condition")
        self.add_input(NodeSocketLogicString, "IP", "ip", {'default_value': "127.0.0.1"})
        self.add_input(NodeSocketLogicIntegerPositive, "Port", 'port', {'default_value': 5005})
        self.add_input(NodeSocketLogicString, "OSC Address", "osc", {'default_value': "/osc"})
        self.add_input(NodeSocketLogicDictionary, "Data", "data")
        
        #Outputs
        self.add_output(NodeSocketLogicCondition, "Done", "DONE")
        
        #Init
        LogicNodeActionType.init(self, context)