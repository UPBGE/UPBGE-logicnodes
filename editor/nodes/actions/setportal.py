from bpy.types import Context, Node, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ..parameters.getportal import LogicNodeGetPortal
from ...nodetree import LogicNodeTree
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicValue
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVector
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicDictionary
from ...sockets import NodeSocketLogicDatablock
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicCollection
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicUI
from ...enum_types import _socket_types
from bpy.props import StringProperty
from bpy.props import EnumProperty
import bpy


@node_type
class LogicNodeSetPortal(LogicNodeActionType):
    bl_idname = "LogicNodeSetPortal"
    bl_label = "Portal In"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "SetPortalNode"
    bl_description = 'Named value'

    def update_draw(self, context=None):
        mode = int(self.mode)
        ipts = self.inputs
        ipts[0].enabled = mode in [0]
        ipts[1].enabled = mode in [1]
        ipts[2].enabled = mode in [2]
        ipts[3].enabled = mode in [3]
        ipts[4].enabled = mode in [4]
        ipts[5].enabled = mode in [5]
        ipts[6].enabled = mode in [6]
        ipts[7].enabled = mode in [7]
        ipts[8].enabled = mode in [8]
        ipts[9].enabled = mode in [9]
        ipts[10].enabled = mode in [10]
        ipts[11].enabled = mode in [11]
        ipts[12].enabled = mode in [12]
        ipts[13].enabled = mode in [13]
        ipts[14].enabled = mode in [14]
        self.color = ipts[mode].draw_color_simple()[:-1]
        self.set_value_type()
        for nodetree in bpy.data.node_groups:
            nodetree.update()
        
    def set_value_type(self):
        portal = self._get_portal()
        if portal is not None:
            portal.socket_type = int(self.mode)

    def _get_portal(self):
        return bpy.context.scene.nl_portals.get(self.get_portal())

    def get_portals(self, context, edit_text):
        if edit_text != '' and edit_text not in [portal.name for portal in bpy.context.scene.nl_portals]:
            yield edit_text
        for portal in context.scene.nl_portals:
            yield (portal.name, 'PLUS')

    def get_portal(self):
        return self.get('portal_prop', '')

    def clear_portal(self, portal):
        if portal is None:
            return
        portal.users -= 1
        if portal.users == 0:
            bpy.context.scene.nl_portals.remove(
                bpy.context.scene.nl_portals.find(portal.name)
            )

    def copy(self, node: Node) -> None:
        portal = self._get_portal()
        if portal is not None:
            portal.users += 1

    def free(self) -> None:
        self.clear_portal(self._get_portal())
        super().free()

    def set_portal(self, value):
        current_portal = self._get_portal()
        new_portal = bpy.context.scene.nl_portals.get(value)
        if value != '' and new_portal is None:
            new_portal = bpy.context.scene.nl_portals.add()
            new_portal.name = value
        if new_portal is not None:
            new_portal.users += 1
        
        def check_tree_type(tree):
            return isinstance(tree, LogicNodeTree)

        def check_node_type(tree):
            return isinstance(tree, LogicNodeGetPortal)

        for tree in filter(check_tree_type, bpy.data.node_groups):
            for node in filter(check_node_type, tree.nodes):
                if current_portal is not None and node.portal == current_portal.name:
                    node.set_portal(value)
        if current_portal is not new_portal:
            if current_portal is not None:
                self.clear_portal(current_portal)

        self['portal_prop'] = value
        self.nl_label = value
        self.set_value_type()
        return None
    
    portal: StringProperty(
        name='Portal',
        get=get_portal,
        set=set_portal,
        search=get_portals,
        search_options={'SUGGESTION'}
    )

    mode: EnumProperty(name='Mode', items=_socket_types, update=update_draw, default='0')

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        col = layout.column(align=True)
        col.prop(self, 'mode', text='')
        col.prop(self, 'portal', text='')

    def init(self, context):
        self.color = (.1, .5, .2)
        self.use_custom_color = True
        self.add_input(NodeSocketLogicValue, "Value", 'value')  # 1
        self.add_input(NodeSocketLogicFloat, "Float", 'value')  # 2
        self.add_input(NodeSocketLogicInteger, "Integer", 'value')  # 3
        self.add_input(NodeSocketLogicString, "String", 'value')  # 4
        self.add_input(NodeSocketLogicBoolean, "Boolean", 'value')  # 5
        self.add_input(NodeSocketLogicVector, "Vector", 'value')  # 6
        self.add_input(NodeSocketLogicColorRGBA, "Color", 'value')  # 7
        self.add_input(NodeSocketLogicList, "List", 'value', shape='SQUARE')  # 8
        self.add_input(NodeSocketLogicDictionary, "Dictionary", 'value', shape='DIAMOND')  # 9
        self.add_input(NodeSocketLogicDatablock, "Datablock", 'value')  # 10
        self.add_input(NodeSocketLogicObject, "Object", 'value')  # 11
        self.add_input(NodeSocketLogicCollection, "Collection", 'value')  # 12
        self.add_input(NodeSocketLogicCondition, "Condition", 'value')  # 13
        self.add_input(NodeSocketLogicPython, "Instance", 'value')  # 14
        self.add_input(NodeSocketLogicUI, "Widget", 'value')  # 15
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        self.set_portal(self['portal_prop'])
        return [('portal', repr(self.portal))]
