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

    def update(self):
        bpy.app.timers.register(self.mark_invalid_links)
        start = time()
        self.changes_staged = True

        # new_inputs = len(self.inputs)
        # new_outputs = len(self.outputs)
        # if self.old_inputs != new_inputs:
        #     self.old_inputs = new_inputs
        # elif self.old_outputs != new_outputs:
        #     self.old_outputs = new_outputs
    
        for n in self.nodes:
            n.update()

        for n in filter(lambda n: isinstance(n, NodeReroute), self.nodes):
            osock = n.inputs[0]
            if not n.inputs[0].links:
                if osock.type != 'VALUE':
                    osock.type = 'VALUE'
                    n.outputs[0].type = 'VALUE'
                    # osock.display_shape = 'CIRCLE'
                    # n.outputs[0].display_shape = 'CIRCLE'
                continue
            socket = osock.links[0].from_socket
            while isinstance(socket.node, NodeReroute):
                now = time()
                if now - start > 3:
                    error('Timeout Error. Check tree for unlinked Reroutes or other issues.')
                    return
                if not socket.node.inputs[0].links:
                    if osock.type != 'VALUE':
                        osock.type = 'VALUE'
                        n.outputs[0].type = 'VALUE'
                        # osock.display_shape = 'CIRCLE'
                        # n.outputs[0].display_shape = osock.nl_shape
                    break
                socket = socket.node.inputs[0].links[0].from_socket
            if osock.type != socket.type:
                osock.type = socket.type
                osock.display_shape = socket.display_shape
                n.outputs[0].type = socket.type
                n.outputs[0].display_shape = socket.display_shape
                osock.type = 'VALUE'  # XXX: Remove, this was for testing
                # print(osock.type, n.outputs[0].type, socket.type)
        for n in filter(lambda n: not isinstance(n, NodeReroute), self.nodes):
            for i in n.inputs:
                if i.is_linked:
                    i.display_shape = i.links[0].from_socket.display_shape
                else:
                    i.display_shape = i.nl_shape
