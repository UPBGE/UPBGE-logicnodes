from bpy.types import Context, NodeTree
from bpy.types import NodeReroute
from bpy.types import NodeInputs
from bpy.types import NodeOutputs
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import CollectionProperty
from bpy.props import BoolProperty
from bpy.props import IntProperty
from ..utilities import make_valid_name
from ..utilities import error
from ..utilities import success
from ..utilities import add_tree_to_active_objects
from ..props.logictreeproperty import LogicNodesLogicTreeProperty
import bpy
from time import time


class LogicNodeTree(NodeTree):
    bl_idname = "BGELogicTree"
    bl_label = "Logic Node Editor"
    bl_icon = "OUTLINER"
    bl_category = "Scripting"

    def group_update(self, context: Context) -> None:
        for n in self.nodes:
            n.group_update(self)

    changes_staged: BoolProperty(default=False)

    type: StringProperty(default='LOGIC')
    old_name: StringProperty()
    properties: CollectionProperty(type=LogicNodesLogicTreeProperty, name='Properties')

    @classmethod
    def poll(cls, context):
        return True

    def get_name(self):
        pass

    def update_name(self, update=True):
        clsname = make_valid_name(self.name)
        if clsname == '':
            error('Tree name cannot consist of illegal letters only!')
            self.name = self.old_name
            return
        if update:
            from ..generator.tree_code_generator import generate_logic_node_code
            generate_logic_node_code()
        if not self.old_name:
            add_tree_to_active_objects(self)
        for obj in bpy.context.scene.objects:
            for ref in obj.logic_trees:
                if ref.tree is self:
                    ref.tree_name = self.name
                    new_comp_name = f'nl_{clsname.lower()}.{clsname}'
                    for i, c in enumerate(obj.game.components):
                        check_name = make_valid_name(self.old_name)
                        if c.name == check_name:
                            active_object = bpy.context.object
                            bpy.context.view_layer.objects.active = obj
                            bpy.ops.logic.python_component_remove(index=i)
                            text = bpy.data.texts.get(f'nl_{check_name.lower()}.py')
                            if text and clsname != check_name:
                                bpy.data.texts.remove(text)
                            prop = obj.game.properties.get(f'NL__{check_name}')
                            if prop:
                                prop.name = f'NL__{clsname}'
                            bpy.ops.logic.python_component_register(component_name=new_comp_name)
                            bpy.context.view_layer.objects.active = active_object

        if self.old_name != '':
            success(f'Successfully Renamed {self.old_name} to {self.name}')
        self.old_name = self.name

    def mark_invalid_links(self):
        '''Mark invalid links, must be called from a timer'''
        for link in self.links:
            if hasattr(link.to_socket, 'validate') and not link.to_socket.skip_validation:
                link.to_socket.validate(link, link.from_socket, self)

    def interface_update(self, context: Context) -> None:
        self.group_update(context)
        return super().interface_update(context)

    def update_draw(self, context):
        for n in self.nodes:
            if hasattr(n, 'update_draw'):
                n.update_draw(context)

    def color_sockets(self):
        for n in filter(lambda n: isinstance(n, NodeReroute), self.nodes):
            outsocket = n.outputs[0]
            insocket = n.inputs[0]

            outlinks = outsocket.links
            inlinks = insocket.links
            if not insocket.is_linked or isinstance(inlinks[0].from_node, NodeReroute):
                # print('trying to source type from another reroute')
                continue
            from_socket = inlinks[0].from_socket
            insocket.type = from_socket.type
            outsocket.type = from_socket.type
            outsocket.display_shape = 'SQUARE'
    
            # print(from_socket.type)
            # print(insocket.type)

    def update(self):
        bpy.app.timers.register(self.mark_invalid_links)
        start = time()
        self.changes_staged = True
    
        for n in self.nodes:
            n.update()
        self.color_sockets()
