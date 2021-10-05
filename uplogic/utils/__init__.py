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
STATUS_INVALID = _Status("INVALID")


LO_AXIS_TO_STRING_CODE = {
    0: "X", 1: "Y", 2: "Z",
    3: "-X", 4: "-Y", 5: "-Z",
}


LO_AXIS_TO_VECTOR = {
    0: Vector((1, 0, 0)), 1: Vector((0, 1, 0)),
    2: Vector((0, 0, 1)), 3: Vector((-1, 0, 0)),
    4: Vector((0, -1, 0)), 5: Vector((0, 0, -1)),
}


def make_valid_name(name):
    valid_characters = (
        "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    clsname = name.replace(' ', '_')
    stripped_name = "".join(
        [c for c in clsname if c in valid_characters]
    )
    return stripped_name


def unload_nodes(a, b):
    if not hasattr(bpy.types.Scene, 'nl_globals_initialized'):
        return
    delattr(bpy.types.Scene, 'nl_globals_initialized')


def is_invalid(*a) -> bool:
    for ref in a:
        if ref is None or ref is STATUS_WAITING or ref == '':
            return True
        if not hasattr(ref, "invalid"):
            continue
        elif ref.invalid:
            return True
    return False


def is_waiting(*args) -> bool:
    if STATUS_WAITING in args:
        return True
    return False


def not_met(*conditions) -> bool:
    for c in conditions:
        if (
            c is STATUS_WAITING or
            c is None or
            c is False
        ):
            return True
    return False


# distance between objects or vectors or tuples. None if not computable
def compute_distance(parama, paramb) -> float:
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


def debug(message: str):
    if not hasattr(bpy.types.Scene, 'logic_node_settings'):
        return
    if not bpy.context or not bpy.context.scene:
        return
    if not bpy.context.scene.logic_node_settings.use_node_debug:
        return
    else:
        print('[Logic Nodes] ' + message)


def interpolate(a: float, b: float, fac: float) -> float:
    if -.001 < a-b < .001:
        return b
    return (fac * b) + ((1-fac) * a)
