# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <An addon to blend Gizmo and Modal operations more seamlessly>
#    Copyright (C) <2022>  <Mat Brady>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

from bpy.types import (
    KeyMapItem
)

from . import (
    operators,
    panels,
    prefs
)

bl_info = {
    "name": "Gizmodal Ops",
    "author": "Mat Brady, Blender Defender",
    "version": (1, 0, 0),
    "blender": (2, 83, 0),
    "location": "3D View > G, R or S",
    "description": "An add-on that seamlessly blends Gizmo and Modal operations.",
    "warning": "",
    "doc_url": "https://github.com/BlenderDefender/Gizmodal-Ops#gizmodal-ops",
    "tracker_url": "https://github.com/BlenderDefender/Gizmodal-Ops/issues",
    "endpoint_url": "https://raw.githubusercontent.com/BlenderDefender/BlenderDefender/updater_endpoints/GIZMODALOPS.json",
    "category": "3D View"
}

modules = (
    operators,
    panels,
    prefs
)


def register_keymap(*args):
    wm = bpy.context.window_manager  # Get the window manager context

    # Get the default keymap for the 3D view
    default_km = wm.keyconfigs.default.keymaps["3D View"]

    # Iterate over all keymap items defined in operators.
    for idname, operator in operators.keymap:
        # Get the Keymap Item from the keymap by searching for the original Operator.
        kmi: KeyMapItem = default_km.keymap_items.find_from_operator(
            idname, include={"KEYBOARD"})

        # If the Keymap Item is not None, rewrite the Operator to the corresponding Gizmodal Ops Operator.
        if kmi:
            kmi.idname = operator.bl_idname


def unregister_keymap(*args):
    wm = bpy.context.window_manager  # Get the window manager context

    # Get the default keymap for the 3D view
    default_km = wm.keyconfigs.default.keymaps["3D View"]

    # Iterate over all keymap items defined in operators.
    for idname, operator in operators.keymap:
        # Get the Keymap Item from the keymap by searching for the Gizmodal Ops Operator.
        kmi: KeyMapItem = default_km.keymap_items.find_from_operator(
            operator.bl_idname, include={"KEYBOARD"})

        # If the Keymap Item is not None, rewrite the Operator to the original Operator.
        if kmi:
            kmi.idname = idname


def register():
    # Register all modules.
    for mod in modules:
        mod.register()

    # Try to register the keymap.
    register_keymap()

    # For safety, if the first method does fail,
    # try to register the keymap 0.1 seconds after Blender loaded properly.
    bpy.app.timers.register(
        register_keymap, first_interval=0.1, persistent=True)


def unregister():
    # Unregister all modules.
    for mod in modules:
        mod.unregister()

    # Try to unregister the "Register Keymap" timer, in case it still is registered.
    try:
        bpy.app.timers.unregister(register_keymap)
    except Exception as e:
        error_message = str(e).lower().replace('error', 'Warning')
        print(
            f"Gizmodal Ops Unregister - {error_message}")

    # Unregister the keymap, so no issues occur after uninstalling Gizmodal Ops.
    unregister_keymap()


# Allow running the script inside of Blenders text editor.
if __name__ == "__main__":
    register()
