from bpy.types import Context, Node, UILayout
from ..node import node_type
from ..node import LogicNodeParameterType
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
import bpy


@node_type
class LogicNodeGetPortal(LogicNodeParameterType):
    bl_idname = "LogicNodeGetPortal"
    bl_label = "Portal Out"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "GetPortalNode"
    bl_description = 'Retrieve a named value'

    def update(self):
        if not self.ready or len(bpy.context.scene.nl_portals) < 1:
            return
        portal = self._get_portal()
        mode = -1 if portal is None else portal.socket_type
        opts = self.outputs
        opts[0].enabled = mode in [0]
        opts[1].enabled = mode in [1]
        opts[2].enabled = mode in [2]
        opts[3].enabled = mode in [3]
        opts[4].enabled = mode in [4]
        opts[5].enabled = mode in [5]
        opts[6].enabled = mode in [6]
        opts[7].enabled = mode in [7]
        opts[8].enabled = mode in [8]
        opts[9].enabled = mode in [9]
        opts[10].enabled = mode in [10]
        opts[11].enabled = mode in [11]
        opts[12].enabled = mode in [12]
        opts[13].enabled = mode in [13]
        opts[14].enabled = mode in [14]
        self.color = opts[mode].draw_color_simple()[:-1]

    def update_draw(self, context=None):
        self.update()

    def _get_portal(self):
        return bpy.context.scene.nl_portals.get(self.get_portal())

    def get_portals(self, context, edit_text):
        for portal in context.scene.nl_portals:
            yield (portal.name, 'PLUS')

    def get_portal(self):
        return self.get('portal_prop', '')

    def set_portal(self, value):
        self['portal_prop'] = value
        self.nl_label = value
        return None
    
    portal: StringProperty(
        name='Portal',
        get=get_portal,
        set=set_portal,
        search=get_portals,
        search_options={'SUGGESTION'},
        update=update_draw
    )

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'portal', text='')

    def init(self, context):
        self.color = (.1, .5, .2)
        self.use_custom_color = True
        self.add_output(NodeSocketLogicValue, "Value", 'VAL', {'enabled': False})  # 0
        self.add_output(NodeSocketLogicFloat, "Float", 'VAL', {'enabled': False})  # 1
        self.add_output(NodeSocketLogicInteger, "Integer", 'VAL', {'enabled': False})  # 2
        self.add_output(NodeSocketLogicString, "String", 'VAL', {'enabled': False})  # 3
        self.add_output(NodeSocketLogicBoolean, "Boolean", 'VAL', {'enabled': False})  # 4
        self.add_output(NodeSocketLogicVector, "Vector", 'VAL', {'enabled': False})  # 5
        self.add_output(NodeSocketLogicColorRGBA, "Color", 'VAL', {'enabled': False})  # 6
        self.add_output(NodeSocketLogicList, "List", 'VAL', {'enabled': False})  # 7
        self.add_output(NodeSocketLogicDictionary, "Dictionary", 'VAL', {'enabled': False})  # 8
        self.add_output(NodeSocketLogicDatablock, "Datablock", 'VAL', {'enabled': False})  # 9
        self.add_output(NodeSocketLogicObject, "Object", 'VAL', {'enabled': False})  # 10
        self.add_output(NodeSocketLogicCollection, "Collection", 'VAL', {'enabled': False})  # 11
        self.add_output(NodeSocketLogicCondition, "Condition", 'VAL', {'enabled': False})  # 12
        self.add_output(NodeSocketLogicPython, "Instance", 'VAL', {'enabled': False})  # 13
        self.add_output(NodeSocketLogicUI, "Widget", 'VAL', {'enabled': False})  # 14
        LogicNodeParameterType.init(self, context)

    def get_attributes(self):
        return [('portal', repr(self.portal))]
