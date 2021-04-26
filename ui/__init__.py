import bpy
import bge_netlogic
import bge_netlogic.utilities as utils
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


def check_double_prop(self, context):
    category = utils.get_global_category()
    props = category.content
    check_double_name(self, props)


def check_double_cat(self, context):
    cats = bpy.context.scene.nl_global_categories
    check_double_name(self, cats)


def check_double_name(self, data):
    name = base = self.name
    names = []
    for p in data:
        if p != self:
            names.append(p.name)
    if base in names:
        count = 1
        name = f'{base}{count}'
        while name in names:
            count += 1
            name = f'{base}{count}'
        self.name = name


_enum_value_types = [
    ("FLOAT", "Float", "A Float value"),
    ("STRING", "String", "A String"),
    ("INTEGER", "Integer", "An Integer value"),
    ("BOOLEAN", "Bool", "A True/False value"),
    ("FILE_PATH", "File Path", 'Choose a file path')
]


class BGEGlobalValue(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name', default='prop', update=check_double_prop)
    value_type: bpy.props.EnumProperty(items=_enum_value_types, name='Value Types')
    string_val: bpy.props.StringProperty(name='String')
    float_val: bpy.props.FloatProperty(name='Floating Point')
    int_val: bpy.props.IntProperty(name='Integer')
    bool_val: bpy.props.BoolProperty(name='Boolean')
    filepath_val: bpy.props.StringProperty(name='File Path', subtype='FILE_PATH')
    persistent: bpy.props.BoolProperty(name='Persistent')


class BGEGlobalValueCategory(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name', default='category', update=check_double_cat)
    content: bpy.props.CollectionProperty(type=BGEGlobalValue)
    selected: bpy.props.IntProperty(name='Value')


class NL_UL_glcategory(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", emboss=False)


class NL_UL_glvalue(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        dat = {
            'STRING': 'string_val',
            'FLOAT': 'float_val',
            'INTEGER': 'int_val',
            'BOOLEAN': 'bool_val',
            'FILE_PATH': 'filepath_val'
        }
        row = layout.split()
        row.prop(item, "name", text="", emboss=False)
        # row.prop(item, 'value_type', text='', emboss=False)
        emboss = item.value_type == 'BOOLEAN' or item.value_type == 'STRING'
        row.prop(item, dat.get(item.value_type, 'FLOAT'), text='', emboss=emboss)


class BGE_PT_GlobalValuePanel(bpy.types.Panel):
    bl_label = "Globals"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGELogicTree.bl_idname)
        return enabled

    def draw(self, context):
        layout = self.layout
        categories = bpy.context.scene.nl_global_categories
        if len(categories) > 0:
            category = utils.get_global_category()
            row = layout.row()
            row.template_list(
                'NL_UL_glcategory',
                '',
                bpy.context.scene,
                'nl_global_categories',
                bpy.context.scene,
                'nl_global_cat_selected',
                rows=3
            )
            opts = row.column(align=True)
            opts.operator(
                bge_netlogic.ops.NLAddGlobalCatOperator.bl_idname,
                text='',
                icon='PLUS'
            )
            opts.operator(
                bge_netlogic.ops.NLRemoveGlobalCatOperator.bl_idname,
                text='',
                icon='REMOVE'
            )
            # Draw Category Properties
            row = layout.row()
            value = utils.get_global_value()
            row.template_list(
                'NL_UL_glvalue',
                '',
                category,
                'content',
                category,
                'selected',
                rows=3
            )
            opts = row.column()
            adders = opts.column(align=True)
            adders.operator(
                bge_netlogic.ops.NLAddGlobalOperator.bl_idname,
                text='',
                icon='PLUS'
            )
            adders.operator(
                bge_netlogic.ops.NLRemoveGlobalOperator.bl_idname,
                text='',
                icon='REMOVE'
            )
            if value:
                opts.prop(value, 'persistent', text='', icon='RADIOBUT_ON' if value.persistent else 'RADIOBUT_OFF')
                row2 = layout.row()
                row2.prop(value, 'value_type', text='Type')
        else:
            layout.operator(
                bge_netlogic.ops.NLAddGlobalCatOperator.bl_idname,
                text='Add Global Category',
                icon='PLUS'
            )


class BGE_PT_GamePropertyPanel(bpy.types.Panel):
    bl_label = "Object Properties"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        enabled = (context.space_data.tree_type == BGELogicTree.bl_idname)
        return ob and ob.name and enabled

    def draw_tree_prop(self, prop, index, box, show_movers):
        col = box.column()
        name = prop.name.split('__')[-1]
        text = 'Logic Tree'
        opts_row = col.row()
        opts_row.label(text=text)
        val_row = col.row()
        val_row.label(text=name)
        val_row.prop(prop, 'value', text='Start')
        if show_movers:
            self.add_movers(index, opts_row)
        opts_row.operator(
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
            is_tree = prop.name.startswith(utils.NLPREFIX)
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
        context.region.tag_redraw()


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
        col = box.column()
        name = prop.name.split('__')[-1]
        text = 'Logic Tree'
        opts_row = col.row()
        opts_row.label(text=text)
        val_row = col.row()
        val_row.label(text=name)
        val_row.prop(prop, 'value', text='Start')
        if show_movers:
            self.add_movers(index, opts_row)
        opts_row.operator(
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
            is_tree = prop.name.startswith(utils.NLPREFIX)
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
        context.region.tag_redraw()


class BGE_PT_LogicNodeSettingsObject(bpy.types.Panel):
    bl_label = "Logic Node Settings"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "physics"
    name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob and ob.name

    def draw(self, context):
        layout = self.layout
        main_col = layout.column()
        parts = main_col.split()
        col1 = parts.column()
        col2 = parts.column()
        col1.prop(context.active_object, 'sound_occluder', text='Sound Occluder')
        col2.prop(context.active_object, 'sound_blocking', text='Factor', slider=True)


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
        col = box.column()
        name = prop.name.split('__')[-1]
        text = 'Logic Tree'
        opts_row = col.row()
        opts_row.label(text=text)
        val_row = col.row()
        val_row.label(text=name)
        val_row.prop(prop, 'value', text='Start')
        if show_movers:
            self.add_movers(index, opts_row)
        opts_row.operator(
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
            is_tree = prop.name.startswith(utils.NLPREFIX)
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
        context.region.tag_redraw()


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
        return enabled

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.scene.nl_group_name, 'name', text='Name')
        pack_new = layout.column()
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


class BGE_PT_LogicTreeOptions(bpy.types.Panel):
    bl_label = "Administration"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Item"
    _current_tree = None

    @classmethod
    def poll(cls, context):
        enabled = (context.space_data.tree_type == BGELogicTree.bl_idname)
        if getattr(context.space_data, 'edit_tree', None) is not None:
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
            text=context.scene.logic_node_settings.tree_compiled,
            icon=utils.STATUS_ICONS.get(context.scene.logic_node_settings.tree_compiled)
        )
        code.operator(
            bge_netlogic.ops.NLGenerateLogicNetworkOperatorAll.bl_idname,
            text="Compile All",
            icon='FILE_SCRIPT'
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
        enabled = (context.space_data.tree_type == BGELogicTree.bl_idname)
        return ob and ob.name and enabled

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
            data.operator(
                bge_netlogic.ops.NLSelectTreeByNameOperator.bl_idname,
                text="Edit",
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
        return enabled

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.4
        layout.operator(
            bge_netlogic.ops.NLBGEDocsButton.bl_idname,
            text="Engine API",
            icon='FILE_BLEND'
        )
        layout.operator(
            bge_netlogic.ops.NLUPBGEDocsButton.bl_idname,
            text="Manual",
            icon='BLENDER'
        )


class BGELogicTree(bpy.types.NodeTree):
    bl_idname = "BGELogicTree"
    bl_label = "Logic Node Editor"
    bl_icon = "OUTLINER"
    bl_category = "Scripting"

    @classmethod
    def poll(cls, context):
        return True

    # def update(self):
    #    if not getattr(bpy.context.scene.logic_node_settings, 'auto_compile'):
    #        return
    #    bge_netlogic.update_current_tree_code()
    #     for link in self.links:
    #         print(link.is_valid)
