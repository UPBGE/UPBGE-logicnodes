import bpy
import bge_netlogic
from os.path import join, dirname


_filter_prop_types = [
    ("TREES", "Logic Trees", "Show only applied Logic Trees"),
    ("FLOAT", "Float Properties", "Show only Float Properties"),
    ("INT", "Int Properties", "Show only Int Properties"),
    ("BOOL", "Boolean Properties", "Show only Boolean Properties"),
    ("STRING", "String Properties", "Show only String Properties"),
    ("TIMER", "Timer Properties", "Show only Timer Properties"),
    ("NAME", 'Filter By Name', 'Search for a Property')
]


def get_icons_directory():

    background = bpy.context.preferences.themes['Default'].view_3d.space.panelcolors.back
    if background[0] < 0.4:
        icons_directory = join(dirname(__file__), "IconsBright")
    else:
        icons_directory = join(dirname(__file__), "IconsDark")

    return icons_directory


class BGEPropFilter(bpy.types.PropertyGroup):
    do_filter: bpy.props.BoolProperty()
    filter_by: bpy.props.EnumProperty(items=_filter_prop_types)
    filter_name: bpy.props.StringProperty()
    show_hidden: bpy.props.BoolProperty(default=True)


class BGEGroupName(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    enabled: bpy.props.BoolProperty()


class BGEGameComponentPanel(bpy.types.Panel):
    bl_label = "Components"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"
    # module = bpy.StringProperty()

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
        column = layout.column()
        column.operator(
            bge_netlogic.ops.NLAddComponentOperator.bl_idname,
            text="Add Component",
            icon='PLUS'
        )


class BGE_PT_GamePropertyPanel(bpy.types.Panel):
    bl_label = "Object Properties"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGELogicTree.bl_idname)
        if enabled and (context.space_data.edit_tree is not None):
            bge_netlogic._consume_update_tree_code_queue()
            if not bge_netlogic._tree_code_writer_started:
                bge_netlogic._tree_code_writer_started = True
                bpy.ops.bgenetlogic.treecodewriter_operator()
        return enabled

    def draw_tree_prop(self, prop, index, box, do_filter):
        row = box.row()
        name = prop.name.split('__')[-1]
        text = 'Applied Tree: {}'.format(name)
        row.label(text=text)
        if not do_filter:
            self.add_movers(index, row)
        row.operator(
                bge_netlogic.ops.NLRemoveTreeByNameOperator.bl_idname,
                text="",
                icon="X"
        ).tree_name = name

    def add_movers(self, index, layout):
        movers = layout.row(align=True)
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
        move_down.direction = 'DOWN'
        move_down.index = move_up.index = index

    def draw(self, context):
        layout = self.layout
        column = layout.column()
        obj = bpy.context.object
        column.operator(
            bge_netlogic.ops.NLAddPropertyOperator.bl_idname,
            text="Add Game Property",
            icon='PLUS'
        )
        options = column.row()
        options.prop(context.scene.prop_filter, 'do_filter', text='Filter Properties')
        options.prop(context.scene.prop_filter, 'show_hidden', text='Show Hidden')
        show_hidden = context.scene.prop_filter.show_hidden
        do_filter = context.scene.prop_filter.do_filter
        prop_type = context.scene.prop_filter.filter_by
        prop_name = context.scene.prop_filter.filter_name
        if do_filter:
            column.prop(context.scene.prop_filter, 'filter_by', text='')
        if prop_type == 'NAME' and do_filter:
            column.prop(context.scene.prop_filter, 'filter_name', text='')
        if not obj:
            return
        props = [prop for prop in obj.game.properties]
        for prop in obj.game.properties:
            if not show_hidden and prop.name.startswith('_'):
                continue
            is_tree = prop.name.startswith('NODELOGIC__')
            has_name = prop_name in prop.name
            if do_filter:
                if prop_type == 'NAME':
                    if not has_name:
                        continue
                elif prop_type == 'TREES':
                    if not is_tree:
                        continue
                elif prop.type != prop_type or is_tree:
                    continue
            index = props.index(prop)
            column.separator()
            box = column.box()
            if is_tree:
                self.draw_tree_prop(prop, index, box, do_filter)
                continue
            entry = box.column()
            row_title = entry.row()
            row_title.prop(prop, 'name', text='')
            row_title.prop(prop, 'show_debug', text='', icon='INFO')
            if not do_filter and show_hidden:
                self.add_movers(index, row_title)
            remove = row_title.operator(
                bge_netlogic.ops.NLRemovePropertyOperator.bl_idname,
                text='',
                icon='X'
            )
            remove.index = index
            row_info = entry.row()
            row_info.prop(prop, 'type', text='')
            row_info.prop(prop, 'value', text='Value')


class BGE_PT_GamePropertyPanel3DView(bpy.types.Panel):
    bl_label = "Object Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def draw_tree_prop(self, prop, index, box, do_filter):
        row = box.row()
        name = prop.name.split('__')[-1]
        text = 'Applied Tree: {}'.format(name)
        row.label(text=text)
        if not do_filter:
            self.add_movers(index, row)
        row.operator(
                bge_netlogic.ops.NLRemoveTreeByNameOperator.bl_idname,
                text="",
                icon="X"
        ).tree_name = name

    def add_movers(self, index, layout):
        movers = layout.row(align=True)
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
        move_down.direction = 'DOWN'
        move_down.index = move_up.index = index

    def draw(self, context):
        layout = self.layout
        column = layout.column()
        obj = bpy.context.object
        column.operator(
            bge_netlogic.ops.NLAddPropertyOperator.bl_idname,
            text="Add Game Property",
            icon='PLUS'
        )
        column.prop(context.scene.prop_filter, 'do_filter', text='Filter Properties')
        do_filter = context.scene.prop_filter.do_filter
        prop_type = context.scene.prop_filter.filter_by
        prop_name = context.scene.prop_filter.filter_name
        if do_filter:
            column.prop(context.scene.prop_filter, 'filter_by', text='')
        if prop_type == 'NAME' and do_filter:
            column.prop(context.scene.prop_filter, 'filter_name', text='')
        if not obj:
            return
        props = [prop for prop in obj.game.properties]
        for prop in obj.game.properties:
            is_tree = prop.name.startswith('NODELOGIC__')
            has_name = prop_name in prop.name
            if do_filter:
                if prop_type == 'NAME':
                    if not has_name:
                        continue
                elif prop_type == 'TREES':
                    if not is_tree:
                        continue
                elif prop.type != prop_type or is_tree:
                    continue
            index = props.index(prop)
            column.separator()
            box = column.box()
            if is_tree:
                self.draw_tree_prop(prop, index, box, do_filter)
                continue
            entry = box.column()
            row_title = entry.row()
            row_title.prop(prop, 'name', text='')
            row_title.prop(prop, 'show_debug', text='', icon='INFO')
            if not do_filter:
                self.add_movers(index, row_title)
            remove = row_title.operator(
                bge_netlogic.ops.NLRemovePropertyOperator.bl_idname,
                text='',
                icon='X'
            )
            remove.index = index
            row_info = entry.row()
            row_info.prop(prop, 'type', text='')
            row_info.prop(prop, 'value', text='Value')


class BGE_PT_PropertiesPanelObject(bpy.types.Panel):
    bl_label = "Game Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def draw_tree_prop(self, prop, index, box, do_filter):
        row = box.row()
        name = prop.name.split('__')[-1]
        text = 'Applied Tree: {}'.format(name)
        row.label(text=text)
        if not do_filter:
            self.add_movers(index, row)
        row.operator(
                bge_netlogic.ops.NLRemoveTreeByNameOperator.bl_idname,
                text="",
                icon="X"
        ).tree_name = name

    def add_movers(self, index, layout):
        movers = layout.row(align=True)
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
        move_down.direction = 'DOWN'
        move_down.index = move_up.index = index

    def draw(self, context):
        layout = self.layout
        column = layout.column()
        obj = bpy.context.object
        column.operator(
            bge_netlogic.ops.NLAddPropertyOperator.bl_idname,
            text="Add Game Property",
            icon='PLUS'
        )
        column.prop(context.scene.prop_filter, 'do_filter', text='Filter Properties')
        do_filter = context.scene.prop_filter.do_filter
        prop_type = context.scene.prop_filter.filter_by
        prop_name = context.scene.prop_filter.filter_name
        if do_filter:
            column.prop(context.scene.prop_filter, 'filter_by', text='')
        if prop_type == 'NAME' and do_filter:
            column.prop(context.scene.prop_filter, 'filter_name', text='')
        if not obj:
            return
        props = [prop for prop in obj.game.properties]
        for prop in obj.game.properties:
            is_tree = prop.name.startswith('NODELOGIC__')
            has_name = prop_name in prop.name
            if do_filter:
                if prop_type == 'NAME':
                    if not has_name:
                        continue
                elif prop_type == 'TREES':
                    if not is_tree:
                        continue
                elif prop.type != prop_type or is_tree:
                    continue
            index = props.index(prop)
            column.separator()
            box = column.box()
            if is_tree:
                self.draw_tree_prop(prop, index, box, do_filter)
                continue
            entry = box.column()
            row_title = entry.row()
            row_title.prop(prop, 'name', text='')
            row_title.prop(prop, 'show_debug', text='', icon='INFO')
            if not do_filter:
                self.add_movers(index, row_title)
            remove = row_title.operator(
                bge_netlogic.ops.NLRemovePropertyOperator.bl_idname,
                text='',
                icon='X'
            )
            remove.index = index
            row_info = entry.row()
            row_info.prop(prop, 'type', text='')
            row_info.prop(prop, 'value', text='Value')


class BGE_PT_LogicTreeGroups(bpy.types.Panel):
    bl_label = "Tree Groups"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"
    _current_tree = None
    new_ver = False

    if not bpy.app.version < (2, 80, 0):
        try:
            icons = bpy.utils.previews.new()
            icons_directory = get_icons_directory()
            icons.load("Icon4Keys", join(icons_directory, "Icon4Keys.png"), 'IMAGE')
            new_ver = True
        except Exception:
            print('Icon can not be set, using original Buttons.')

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
        pack_new = layout.row()
        pack_new.scale_y = 1.4
        pack_new.operator(
            bge_netlogic.ops.NLMakeGroupOperator.bl_idname,
            icon='IMPORT'
        )
        layout.separator()
        prefabs = layout.box()
        title = prefabs.box()
        title.label(text='Node Prefabs:')
        template_col = prefabs.column()
        template_col.scale_y = 1.4
        if self.new_ver:
            template_col.operator(
                bge_netlogic.ops.NLAdd4KeyTemplateOperator.bl_idname,
                icon_value=self.icons["Icon4Keys"].icon_id,
            )
        else:
            template_col.operator(
                bge_netlogic.ops.NLAdd4KeyTemplateOperator.bl_idname,
                icon='LAYER_ACTIVE'
            )


class BGE_PT_LogicTreeInfoPanel(bpy.types.Panel):
    bl_label = "Object Trees"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"
    _current_tree = None
    new_ver = False

    if not bpy.app.version < (2, 80, 0):
        try:
            icons = bpy.utils.previews.new()
            icons_directory = get_icons_directory()
            icons.load("IconApply", join(icons_directory, "IconApply.png"), 'IMAGE')
            new_ver = True
        except Exception:
            print('Icon can not be set, using original Buttons.')

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
                return None
                # None means undefined, mixed,
                # some are enabled, some are disabled
        return last

    def draw(self, context):
        layout = self.layout
        apply_col = layout.column()
        apply_col.scale_y = 1.4
        apply = apply_col.box()
        if self.new_ver:
            apply.operator(
                bge_netlogic.ops.NLApplyLogicOperator.bl_idname,
                icon_value=self.icons["IconApply"].icon_id,
                text="Apply To Selected"
            ).owner = "BGE_PT_LogicPanel"
        else:
            apply.operator(
                bge_netlogic.ops.NLApplyLogicOperator.bl_idname,
                text="Apply To Selected",
                icon='PREFERENCES'
            ).owner = "BGE_PT_LogicPanel"
        code = layout.box()
        code.operator(
            bge_netlogic.ops.NLGenerateLogicNetworkOperator.bl_idname,
            text="Update Code",
            icon='FILE_SCRIPT'
        )
        code.operator(
            bge_netlogic.ops.NLGenerateLogicNetworkOperatorAll.bl_idname,
            text="Generate All Code",
            icon='SCRIPTPLUGINS'
        )
        layout.separator()
        selected_objects = [
            ob for ob in context.scene.objects if ob.select_get()
        ] if not bpy.app.version < (2, 80, 0) else [
            ob for ob in context.scene.objects if ob.select
        ]
        active_tree_items = {}
        if context.object:
            box_over = layout.box()
            box_over.label(
                text="Trees applied to {}:".format(context.object.name)
            )
        for ob in selected_objects:
            for e in ob.bgelogic_treelist:
                data = active_tree_items.get(e.tree_name)
                if data is None:
                    data = []
                    active_tree_items[e.tree_name] = data
                data.append(e)
        for name in active_tree_items:
            box = box_over.box()
            status = self.get_combined_status_of_tree_items(
                active_tree_items[name]
            )
            status_icon = "CHECKBOX_DEHLT"
            if status is None:
                status_icon = "QUESTION"
                status = False
                # For mixed states, apply means "set it to enabled"
            elif status is True:
                status_icon = "CHECKBOX_HLT"
            col = box.column()
            row = col.row(align=False)
            row.label(text='Node Tree: {}'.format(name))
            row.operator(
                bge_netlogic.ops.NLRemoveTreeByNameOperator.bl_idname,
                text="",
                icon="X"
            ).tree_name = name
            data = col.row(align=False)
            op_data = data.operator(
                bge_netlogic.ops.NLSwitchInitialNetworkStatusOperator.bl_idname,
                text="Use at Startup",
                icon=status_icon
            )
            op_data.tree_name = name
            op_data.current_status = status
            data.operator(
                bge_netlogic.ops.NLSelectTreeByNameOperator.bl_idname,
                text="Edit this Tree",
                icon="NODETREE"
            ).tree_name = name


class BGE_PT_LogicPanel(bpy.types.Panel):
    bl_label = "Custom Nodes"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Custom Nodes"
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
        layout.scale_y = 1.4
        layout.operator(
            bge_netlogic.ops.NLPopupTemplatesOperator.bl_idname,
            text="Custom Nodes Templates..."
        )
        layout.operator(
            bge_netlogic.ops.NLImportProjectNodes.bl_idname,
            text="Import Custom Nodes"
        )
        layout.operator(
            bge_netlogic.ops.NLLoadProjectNodes.bl_idname,
            text="Refresh Imported Nodes"
        )


class BGE_PT_HelpPanel(bpy.types.Panel):
    bl_label = "Help & Documentation"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Help & Documentation"
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
        layout.scale_y = 1.4
        layout.operator(
            bge_netlogic.ops.NLBGEDocsButton.bl_idname,
            text="Blender Game Engine",
            icon='MENU_PANEL'
        )
        layout.operator(
            bge_netlogic.ops.NLUPBGEDocsButton.bl_idname,
            text="UPBGE",
            icon='MENU_PANEL'
        )
        layout.operator(
            bge_netlogic.ops.NLDocsButton.bl_idname,
            text="Logic Nodes",
            icon='OUTLINER'
        )


def update_tree_code(self, context):
    bge_netlogic.update_current_tree_code()


class BGELogicTree(bpy.types.NodeTree):
    bl_idname = "BGELogicTree"
    bl_label = "Logic Tree Editor"
    bl_icon = "OUTLINER" if not bpy.app.version < (2, 80, 0) else 'PLUS'
    bl_category = "Scripting"

    @classmethod
    def poll(cls, context):
        return True

    def update(self):
        bge_netlogic.update_current_tree_code()
