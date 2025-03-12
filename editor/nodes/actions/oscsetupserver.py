from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicDictionary
from ...sockets import NodeSocketLogicBoolean

@node_type
class LogicNodeOSCSetupServer(LogicNodeActionType):
    bl_idname = "LogicNodeOSCSetupServer"
    bl_label = "Setup OSC Server"
    bl_description = 'Manage an Open Sound Control (OSC) server'
    bl_width_default = 180
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULOSCSetupServer"
    
    def init(self, context):
        #Inputs
        self.add_input(NodeSocketLogicCondition, "Start", "condition_start")
        self.add_input(NodeSocketLogicCondition, "Stop", "condition_stop")
        self.add_input(NodeSocketLogicString, "IP", "ip", {'default_value': "127.0.0.1"})
        self.add_input(NodeSocketLogicIntegerPositive, "Port", "port", {'default_value': 9001})
        #(Remove OSC Filter)
        self.add_input(NodeSocketLogicString, "Default Address", "default_address", {'default_value': "/osc"})
        self.add_input(NodeSocketLogicBoolean, "Debug", "debug")
        
        #Oututs
        self.add_output(NodeSocketLogicDictionary, "Messages", "MESSAGES")
        
        #Init
        LogicNodeActionType.init(self, context)