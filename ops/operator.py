from bpy.types import Operator
from ..utilities import error, preferences
from ..generator.tree_code_generator import generate_logic_node_code
import time
import bpy
import os


_tree_code_writer_started = False

_operators = []


def operator(obj: Operator) -> Operator:
    _operators.append(obj)
    return obj


_update_queue = []


def _consume_update_tree_code_queue():
    if not _update_queue:
        return
    now = time.time()
    last_event = _update_queue[-1]
    delta = now - last_event
    if delta > 0.25:
        _update_queue.clear()
        generate_logic_node_code()
        return True


def update_current_tree_code(*ignored):
    global _tree_code_writer_started
    if not _tree_code_writer_started:
        _tree_code_writer_started = True
        generate_logic_node_code()
    now = time.time()
    _update_queue.append(now)


def _enum_components(self, context):
    select_text = context.scene.componenthelper
    items = []
    for line in select_text.lines:
        if 'class ' in line.body:
            cname = line.body.split('(')[0]
            cname = cname.split('class ')[-1]
            cname = cname.replace(':', '')
            cname = cname.replace(' ', '')
            items.append((cname, cname, cname))
    return items


def reload_texts():
    for t in bpy.data.texts:
        if t.filepath:
            path = (
                os.path.join(bpy.path.abspath('//'), t.filepath[2:])
                if t.filepath.startswith('//')
                else t.filepath
            )
            with open(path) as f:
                t.clear()
                t.write(f.read())
