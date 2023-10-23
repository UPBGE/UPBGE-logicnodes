import bpy
from .nodetree import LogicNodeTree


def filter_materials(self, item):
    if item.is_grease_pencil:
        return False
    return True


def filter_geometry_nodes(self, item):
    if isinstance(item, bpy.types.GeometryNodeTree):
        return True
    return False


def filter_lights(self, item):
    if (
        isinstance(item.data, bpy.types.AreaLight)
        or isinstance(item.data, bpy.types.PointLight)
        or isinstance(item.data, bpy.types.SpotLight)
        or isinstance(item.data, bpy.types.SunLight)
    ):
        return True
    return False


def filter_texts(self, item):
    if (
        item.name.startswith('nl_')
    ):
        return False
    return True


def filter_navmesh(self, item):
    if item.game.physics_type == 'NAVMESH':
        return True
    return False


def filter_camera(self, item):
    if isinstance(item.data, bpy.types.Camera):
        return True
    return False


def filter_speaker(self, item):
    if isinstance(item.data, bpy.types.Speaker):
        return True
    return False


def filter_armatures(self, item):
    if (
        isinstance(item.data, bpy.types.Armature)
    ):
        return True
    return False


def filter_curves(self, item):
    if (
        isinstance(item.data, bpy.types.Curve)
    ):
        return True
    return False


def filter_logic_trees(self, item):
    if (
        isinstance(item, LogicNodeTree)
    ):
        return True
    return False


def filter_node_groups(self, item):
    if (
        isinstance(item, bpy.types.ShaderNodeTree)
    ):
        return True
    return False
