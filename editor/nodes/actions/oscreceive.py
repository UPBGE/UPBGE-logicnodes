from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicDictionary
from ...sockets import NodeSocketLogicParameter

@node_type
class LogicNodeOSCReceive(LogicNodeActionType):
    bl_idname = "LogicNodeOSCReceive"
    bl_label = "Receive OSC Message"
    bl_description = "Receive OSC messages from a given address"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULOSCReceive"
    
    def init(self, context):
        #Inputs
        self.add_input(NodeSocketLogicDictionary, "Messages", "messages")
        self.add_input(NodeSocketLogicString, "OSC Address", "osc_address", {'default_value':"/osc"})
        
        #Outputs
        self.add_output(NodeSocketLogicCondition, "Received", "RECEIVED")
        self.add_output(NodeSocketLogicParameter, "Value", "VALUE")
        
        #Init
        LogicNodeActionType.init(self, context)