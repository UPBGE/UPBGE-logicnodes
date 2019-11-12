import bpy
import bge_netlogic


class BGEGamePropertyPanel(bpy.types.Panel):
    bl_label = "Object Properties"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    name = bpy.props.StringProperty()

    def draw(self, context):
        layout = self.layout
        column = layout.column()
        obj = bpy.context.object
        column.operator(
            bge_netlogic.ops.NLAddPropertyOperator.bl_idname,
            text="Add Game Property",
            icon='PLUS'
            )
        props = [prop for prop in obj.game.properties]
        for prop in obj.game.properties:
            box = column.box()
            entry = box.column()
            row_title = entry.row()
            row_title.prop(prop, 'name', text='')
            row_title.prop(prop, 'show_debug', text='', icon='INFO')
            movers = row_title.row(align=True)
            move_up = movers.operator(
                bge_netlogic.ops.NLMovePropertyOperator.bl_idname,
                text='',
                icon='TRIA_UP'
            )
            move_up.direction = 'UP'
            move_down = movers.operator(
                bge_netlogic.ops.NLMovePropertyOperator.bl_idname,
                text='',
                icon='TRIA_DOWN'
            )
            remove = row_title.operator(
                bge_netlogic.ops.NLRemovePropertyOperator.bl_idname,
                text='',
                icon='X'
            )
            move_down.direction = 'DOWN'
            remove.index = move_down.index = move_up.index = props.index(prop)
            row_info = entry.row()
            row_info.prop(prop, 'type', text='')
            row_info.prop(prop, 'value', text='Value')
            column.separator()


class BGELogicTreeInfoPanel(bpy.types.Panel):
    bl_label = "Applied Objects"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGELogicTree.bl_idname)
        if enabled and (context.space_data.edit_tree is not None):
            bge_netlogic._consume_update_tree_code_queue()
            if not bge_netlogic._tree_code_writer_started:
                bge_netlogic._tree_code_writer_started = True
                bpy.ops.bgenetlogic.treecodewriter_operator()
        return enabled

    def get_combined_status_of_tree_items(self, tree_item_list):
        last = None
        for e in tree_item_list:
            initial_status = e.tree_initial_status
            if last is None:
                last = initial_status
            elif last != initial_status:
                return None  # None means undefined, mixed, some are enabled, some are disabled
        return last

    def draw(self, context):
        layout = self.layout
        layout.operator(bge_netlogic.ops.NLApplyLogicOperator.bl_idname, text="Apply To Selected").owner = "BGELogicPanel"
        layout.separator()
        layout.operator(bge_netlogic.ops.NLGenerateLogicNetworkOperator.bl_idname, text="Update Code")
        selected_objects = [ob for ob in context.scene.objects if ob.select_get()]
        active_tree_items = {}
        box_over = layout.box()
        box_over.label(text="Trees applied to {}".format(context.object.name))
        for ob in selected_objects:
            for e in ob.bgelogic_treelist:
                data = active_tree_items.get(e.tree_name)
                if data is None:
                    data = []
                    active_tree_items[e.tree_name] = data
                data.append(e)
        for name in active_tree_items:
            box = box_over.box()
            status = self.get_combined_status_of_tree_items(active_tree_items[name])
            status_icon = "CHECKBOX_DEHLT"
            if status is None:
                status_icon = "QUESTION"
                status = False  # For mixed states, apply means "set it to enabled"
            elif status is True:
                status_icon = "CHECKBOX_HLT"
            col = box.column()
            row = col.row(align=False)
            row.label(text='Node Tree: {}'.format(name))
            row.operator(bge_netlogic.ops.NLRemoveTreeByNameOperator.bl_idname, text="", icon="X").tree_name = name
            data = col.row(align=False)
            op_data = data.operator(bge_netlogic.ops.NLSwitchInitialNetworkStatusOperator.bl_idname, text="Use at Startup", icon=status_icon)
            op_data.tree_name = name
            op_data.current_status = status
            data.operator(bge_netlogic.ops.NLSelectTreeByNameOperator.bl_idname, text="Edit this Tree", icon="NODETREE").tree_name = name
        pass

class BGELogicPanel(bpy.types.Panel):
    bl_label = "Custom Nodes"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_options = {'DEFAULT_CLOSED'}
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGELogicTree.bl_idname)
        if enabled and (context.space_data.edit_tree is not None):
            bge_netlogic._consume_update_tree_code_queue()
            if not bge_netlogic._tree_code_writer_started:
                bge_netlogic._tree_code_writer_started = True
                bpy.ops.bgenetlogic.treecodewriter_operator()
        return enabled

    def draw(self, context):
        layout = self.layout
        layout.operator(bge_netlogic.ops.NLPopupTemplatesOperator.bl_idname, text="Custom Nodes Templates...")
        layout.operator(bge_netlogic.ops.NLImportProjectNodes.bl_idname, text="Import Custom Nodes")
        layout.operator(bge_netlogic.ops.NLLoadProjectNodes.bl_idname, text="Refresh Imported Nodes")
        pass


def update_tree_code(self, context):
    bge_netlogic.update_current_tree_code()


class BGELogicTree(bpy.types.NodeTree):
    bl_idname = "BGELogicTree"
    bl_label = "Logic Tree Editor"
    bl_icon = "OUTLINER"
    bl_type = "Scripting"

    @classmethod
    def poll(cls, context):
        return True

    def update(self):
        bge_netlogic.update_current_tree_code()