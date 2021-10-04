from mathutils import Vector
import bpy


class _Status(object):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return self._name


NO_VALUE = _Status("NO_VALUE")
STATUS_WAITING = _Status("WAITING")
STATUS_READY = _Status("READY")


def unload_nodes(a, b):
    if not hasattr(bpy.types.Scene, 'nl_globals_initialized'):
        return
    delattr(bpy.types.Scene, 'nl_globals_initialized')


def is_invalid(*a):
    for ref in a:
        if ref is None or ref is STATUS_WAITING or ref == '':
            return True
        if not hasattr(ref, "invalid"):
            continue
        elif ref.invalid:
            return True
    return False


# distance between objects or vectors or tuples. None if not computable
def compute_distance(parama, paramb):
    if is_invalid(parama):
        return None
    if is_invalid(paramb):
        return None
    if hasattr(parama, "getDistanceTo"):
        return parama.getDistanceTo(paramb)
    if hasattr(paramb, "getDistanceTo"):
        return paramb.getDistanceTo(parama)
    va = Vector(parama)
    vb = Vector(paramb)
    return (va - vb).length


def debug(message):
    if not hasattr(bpy.types.Scene, 'logic_node_settings'):
        return
    if not bpy.context or not bpy.context.scene:
        return
    if not bpy.context.scene.logic_node_settings.use_node_debug:
        return
    else:
        print('[Logic Nodes] ' + message)
