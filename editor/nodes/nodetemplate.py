from bge_netlogic import node_type
from bge_netlogic.editor.nodes.node import LogicNodeCustomType
from bge_netlogic.editor.sockets import *  # import all socket types


# the @node_type decorator automatically registers this node-type
# once it has been imported.
@node_type
class LogicNodeCustomNode(LogicNodeCustomType):
    # `bl_idname` has to stay the same through later versions. Nodes
    # are registered under this ID, so if it changes, blender
    # cannot find nodes added by older versions
    bl_idname = 'LogicNodeCustomNode'
    bl_label = 'My Custom Node'

    # `nl_module` defines the module (python file) where the game-side
    # implementation of the node is found.
    nl_module = 'my_custom_package.nodes'
    # `nl_class` defines the class to be instantiated and run in-game.
    nl_class = 'MyCustomNode'

    def init(self, context):
        # Add your inputs/outputs here like this:
        #    self.add_input(SOCKET_CLASS_NAME, SOCKET_DISPLAY_NAME, LOGIC_ATTRIBUTE_NAME)
        # SOCKET_CLASS_NAME: This defines the type of the socket
        # SOCKET_DISPLAY_NAME: This string will be shown next to the socket
        # LOGIC_ATTRIBUTE_NAME: This is the corresponding attribute name in the game-side implementation
        self.add_input(NodeSocketLogicObject, 'Object', 'game_object')
        self.add_output(NodeSocketLogicString, 'Name', 'NAME')

        # call the superclass constructor last, because this marks the
        # node as "ready" for the editor.
        LogicNodeCustomType.init(self, context)
