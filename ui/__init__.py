import bpy
import bge_netlogic
from os.path import join, dirname


_filter_prop_types = [
    ("TREES", "Logic Trees", "Show only applied Logic Trees"),
    ("FLOAT", "Floats", "Show only Float Properties"),
    ("INT", "Integers", "Show only Int Properties"),
    ("BOOL", "Booleans", "Show only Boolean Properties"),
    ("STRING", "Strings", "Show only String Properties"),
    ("TIMER", "Timers", "Show only Timer Properties"),
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
    do_filter: bpy.props.BoolProperty(
        name='Filter',
        description='Filter properties by type or name'
    )
    filter_by: bpy.props.EnumProperty(
        items=_filter_prop_types
    )
    filter_name: bpy.props.StringProperty(name='Property Name')
    show_hidden: bpy.props.BoolProperty(
        name='Show Hidden',
        default=True,
        description='Show properties that start with "_"'
    )
    show_trees: bpy.props.BoolProperty(
        name='Show Trees',
        default=True,
        description='Show applied logic trees'
    )
    collapse_trees: bpy.props.BoolProperty(
        name='Collapse Trees',
        default=True,
        description='Compress Logic Tree Properties to an immutable form (recommended)'
    )


class BGEGroupName(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(default='NewTree')
    enabled: bpy.props.BoolProperty()


class BGE_PT_GameComponentPanel(bpy.types.Panel):
    bl_label = "Components"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"
    # module = bpy.StringProperty()

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob and ob.name

    def draw(self, context):
        layout = self.layout

        ob = context.active_object
        game = ob.game

        row = layout.row()
        row.operator("logic.python_component_register", text="Register", icon="PLUS")
        row.operator("logic.python_component_create", text="Create", icon="PLUS")

        for i, c in enumerate(game.components):
            box = layout.box()
            row = box.row()
            row.prop(c, "show_expanded", text="", emboss=False)
            row.label(text=c.name)
            row.operator("logic.python_component_reload", text="", icon='RECOVER_LAST').index = i
            row.operator("logic.python_component_remove", text="", icon='X').index = i

            if c.show_expanded and len(c.properties) > 0:
                box = box.box()
                for prop in c.properties:
                    row = box.row()
                    row.label(text=prop.name)
                    col = row.column()
                    col.prop(prop, "value", text="")


class BGE_PT_GamePropertyPanel(bpy.types.Panel):
    bl_label = "Object Properties"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob and ob.name

    def draw_tree_prop(self, prop, index, box, show_movers):
        row = box.row()
        name = prop.name.split('__')[-1]
        text = 'Logic Tree'
        row.label(text=text)
        name_label = box.row()
        name_label.scale_y = .7
        name_label.label(text=name)
        if show_movers:
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
        show_hidden = context.scene.prop_filter.show_hidden
        collapse_trees = context.scene.prop_filter.collapse_trees
        do_filter = context.scene.prop_filter.do_filter
        prop_type = context.scene.prop_filter.filter_by
        prop_name = context.scene.prop_filter.filter_name
        show_trees = context.scene.prop_filter.show_trees

        hide_icon = 'HIDE_OFF' if show_hidden else 'HIDE_ON'
        collapse_icon = 'LOCKED' if collapse_trees else 'UNLOCKED'
        options.prop(
            context.scene.prop_filter,
            'do_filter',
            icon='FILTER',
            text=''
        )
        options.prop(
            context.scene.prop_filter,
            'show_hidden',
            icon=hide_icon,
            text=''
        )
        options.prop(
            context.scene.prop_filter, 
            'show_trees',
            icon='OUTLINER',
            text=''
        )
        options.prop(
            context.scene.prop_filter,
            'collapse_trees',
            icon=collapse_icon,
            text=''
        )

        if do_filter:
            column.prop(context.scene.prop_filter, 'filter_by', text='')
        if prop_type == 'NAME' and do_filter:
            column.prop(
                context.scene.prop_filter,
                'filter_name',
                text='',
                icon='VIEWZOOM'
            )
        if not obj:
            return

        show_movers = show_hidden and show_trees and not do_filter

        props = [prop for prop in obj.game.properties]
        for prop in obj.game.properties:
            if not show_hidden and prop.name.startswith('_'):
                continue
            is_tree = prop.name.startswith('NODELOGIC__')
            if is_tree and not show_trees:
                continue
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
            if is_tree and collapse_trees:
                self.draw_tree_prop(prop, index, box, show_movers)
                continue
            entry = box.column()
            row_title = entry.row()
            row_title.prop(prop, 'name', text='')
            row_title.prop(prop, 'show_debug', text='', icon='INFO')
            if show_movers:
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
        ob = context.active_object
        return ob and ob.name

    def draw_tree_prop(self, prop, index, box, show_movers):
        row = box.row()
        name = prop.name.split('__')[-1]
        text = 'Logic Tree'
        row.label(text=text)
        name_label = box.row()
        name_label.scale_y = .7
        name_label.label(text=name)
        if show_movers:
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
        show_hidden = context.scene.prop_filter.show_hidden
        collapse_trees = context.scene.prop_filter.collapse_trees
        do_filter = context.scene.prop_filter.do_filter
        prop_type = context.scene.prop_filter.filter_by
        prop_name = context.scene.prop_filter.filter_name
        show_trees = context.scene.prop_filter.show_trees

        hide_icon = 'HIDE_OFF' if show_hidden else 'HIDE_ON'
        collapse_icon = 'CHECKBOX_DEHLT' if collapse_trees else 'OBJECT_HIDDEN'
        options.prop(context.scene.prop_filter, 'do_filter', icon='FILTER', text='')
        options.prop(context.scene.prop_filter, 'show_hidden', icon=hide_icon, text='')
        options.prop(context.scene.prop_filter, 'show_trees', icon='OUTLINER', text='')
        options.prop(context.scene.prop_filter, 'collapse_trees', icon=collapse_icon, text='')

        if do_filter:
            column.prop(context.scene.prop_filter, 'filter_by', text='')
        if prop_type == 'NAME' and do_filter:
            column.prop(context.scene.prop_filter, 'filter_name', text='', icon='VIEWZOOM')
        if not obj:
            return

        show_movers = show_hidden and show_trees and not do_filter

        props = [prop for prop in obj.game.properties]
        for prop in obj.game.properties:
            if not show_hidden and prop.name.startswith('_'):
                continue
            is_tree = prop.name.startswith('NODELOGIC__')
            if is_tree and not show_trees:
                continue
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
            if is_tree and collapse_trees:
                self.draw_tree_prop(prop, index, box, show_movers)
                continue
            entry = box.column()
            row_title = entry.row()
            row_title.prop(prop, 'name', text='')
            row_title.prop(prop, 'show_debug', text='', icon='INFO')
            if show_movers:
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
        ob = context.active_object
        return ob and ob.name

    def draw_tree_prop(self, prop, index, box, show_movers):
        row = box.row()
        name = prop.name.split('__')[-1]
        text = 'Logic Tree'
        row.label(text=text)
        name_label = box.row()
        name_label.scale_y = .7
        name_label.label(text=name)
        if show_movers:
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
        show_hidden = context.scene.prop_filter.show_hidden
        collapse_trees = context.scene.prop_filter.collapse_trees
        do_filter = context.scene.prop_filter.do_filter
        prop_type = context.scene.prop_filter.filter_by
        prop_name = context.scene.prop_filter.filter_name
        show_trees = context.scene.prop_filter.show_trees

        hide_icon = 'HIDE_OFF' if show_hidden else 'HIDE_ON'
        collapse_icon = 'CHECKBOX_DEHLT' if collapse_trees else 'OBJECT_HIDDEN'
        options.prop(context.scene.prop_filter, 'do_filter', icon='FILTER', text='')
        options.prop(context.scene.prop_filter, 'show_hidden', icon=hide_icon, text='')
        options.prop(context.scene.prop_filter, 'show_trees', icon='OUTLINER', text='')
        options.prop(context.scene.prop_filter, 'collapse_trees', icon=collapse_icon, text='')

        if do_filter:
            column.prop(context.scene.prop_filter, 'filter_by', text='')
        if prop_type == 'NAME' and do_filter:
            column.prop(context.scene.prop_filter, 'filter_name', text='', icon='VIEWZOOM')
        if not obj:
            return

        show_movers = show_hidden and show_trees and not do_filter

        props = [prop for prop in obj.game.properties]
        for prop in obj.game.properties:
            if not show_hidden and prop.name.startswith('_'):
                continue
            is_tree = prop.name.startswith('NODELOGIC__')
            if is_tree and not show_trees:
                continue
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
            if is_tree and collapse_trees:
                self.draw_tree_prop(prop, index, box, show_movers)
                continue
            entry = box.column()
            row_title = entry.row()
            row_title.prop(prop, 'name', text='')
            row_title.prop(prop, 'show_debug', text='', icon='INFO')
            if show_movers:
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
    bl_label = "Tree Prefabs and Subtrees"
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
        pack_new = layout.column()
        pack_new.scale_y = 1.4
        pack_new.operator(
            bge_netlogic.ops.NLMakeGroupOperator.bl_idname,
            icon='IMPORT'
        )
        layout.prop(bpy.context.scene.nl_group_name, 'name', text='Name')

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


class BGE_PT_LogicTreeOptions(bpy.types.Panel):
    bl_label = "Administration"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"
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
        apply_col = layout.column()
        apply_col.scale_y = 1.4
        apply = apply_col.box()
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
        ob = context.active_object
        return ob and ob.name

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
        selected_objects = [
            ob for ob in context.scene.objects if ob.select_get()
        ] if not bpy.app.version < (2, 80, 0) else [
            ob for ob in context.scene.objects if ob.select
        ]
        active_tree_items = {}
        title = None
        if context.object:
            box_over = layout.box()
            title = box_over.row()
        for ob in selected_objects:
            for e in ob.bgelogic_treelist:
                data = active_tree_items.get(e.tree_name)
                if data is None:
                    data = []
                    active_tree_items[e.tree_name] = data
                data.append(e)
        tree_count = len(active_tree_items.keys())
        if title:
            title.label(text="Trees applied to {}: {}".format(context.object.name, tree_count))
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
            icon='FILE_BLEND'
        )
        layout.operator(
            bge_netlogic.ops.NLUPBGEDocsButton.bl_idname,
            text="UPBGE",
            icon='BLENDER'
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
