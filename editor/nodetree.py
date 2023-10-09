from bpy.types import NodeTree
from bpy.types import NodeReroute
from bpy.props import StringProperty
from ..utilities import make_valid_name
from ..utilities import error
from ..utilities import success
import bpy
from time import time


class LogicNodeTree(NodeTree):
    bl_idname = "BGELogicTree"
    bl_label = "Logic Node Editor"
    bl_icon = "OUTLINER"
    bl_category = "Scripting"
    old_name: StringProperty()
    old_links = []

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
            bpy.ops.logic_nodes.generate_code()
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
            if hasattr(link.to_socket, 'validate'):
                link.to_socket.validate(link, link.from_socket)

    def update(self):
        bpy.app.timers.register(self.mark_invalid_links)
        start = time()
        for n in self.nodes:
            if isinstance(n, NodeReroute):
                osock = n.inputs[0]
                if not n.inputs[0].links:
                    if osock.type != 'VALUE':
                        osock.type = 'VALUE'
                        n.outputs[0].type = 'VALUE'
                        osock.display_shape = 'CIRCLE'
                        n.outputs[0].display_shape = 'CIRCLE'
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
                            osock.display_shape = 'CIRCLE'
                            n.outputs[0].display_shape = 'CIRCLE'
                        break
                    socket = socket.node.inputs[0].links[0].from_socket
                if osock.type != socket.type:
                    osock.type = socket.type
                    osock.display_shape = socket.display_shape
                    n.outputs[0].type = socket.type
                    n.outputs[0].display_shape = socket.display_shape
