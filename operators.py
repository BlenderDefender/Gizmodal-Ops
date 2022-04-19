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
    Operator,
    Context,
    Event
)

import time


class GIZMODAL_OPS_OT_base(Operator):
    # class GIZMODAL_OPS_OT_move(Operator):  # ! DEBUGGING ONLY
    """Base operator"""
    bl_idname = "gizmodal_ops.base"
    bl_label = "Base"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self) -> None:
        super().__init__()
        # How many pixels the mouse has to be moved before triggering the modal operator.
        self.mouse_pixel_error = 0  # TODO: Make this a setting.
        self.time_window = 2  # TODO: Make this a setting.

        # Default the key to None
        # self.key = None
        # self.key = "G"  # ! DEBUGGING ONLY

        # Define a dictionary of keys that may be pressed within the time window
        # after the initial keypress.
        self.other_keys = {
            "X": {"shift": True, "constraint_axis": (True, False, False)},
            "Y": {"shift": True, "constraint_axis": (False, True, False)},
            "Z": {"shift": True, "constraint_axis": (False, False, True)}
        }

    def execute(self, context: Context):
        # Set the Operator "phase" to KEYPRESS:
        # In this phase, Gizmodal Ops waits for either a mouse move
        # or a release event.
        self.phase = "KEYPRESS"

        # Switch to the Gizmo.
        self._gizmo_function()

        # Run this operator in modal mode.
        context.window_manager.modal_handler_add(self)

        return {"RUNNING_MODAL"}

    def modal(self, context: Context, event: Event):
        # While the key is pressed down, check for mouse moves and RELEASE events.
        if self.phase == "KEYPRESS":
            return self.keypress_phase(context, event)

        # If the time window is over, stop the execution of Gizmodal Ops.
        if time.time() - self.start_time >= self.time_window:
            return {"FINISHED"}

        # #Ignore certain key events. It looks like there is no reason to do so...
        # #if event.type in ["MOUSEMOVE", "RIGHT_SHIFT", "LEFT_SHIFT", "TIMER"]:
        # #    return {"RUNNING_MODAL"}

        # Check, if the key is one of the additional keys that may be pressed in the time window.
        if event.type in self.other_keys.keys():
            key = self.other_keys[event.type]

            is_pure_keypress = self._compare_keypress(event, event.type)
            is_keypress_with_shift = self._compare_keypress(
                event, event.type, shift=True)

            # Abort, if the keypress is neither a pure keypress nor with a shift key pressed.
            # If the shift key is pressed, abort if the configuration doesn't allow the shift key to be pressed.
            if not (is_pure_keypress or (is_keypress_with_shift and key["shift"])):
                return {"PASS_THROUGH"}

            # Get the constraint axis from the key.
            constraint_axis = key["constraint_axis"]

            # Invert the constraint axis, if the shift key is pressed.
            if is_keypress_with_shift:
                constraint_axis = tuple([not el for el in constraint_axis])

            # Invoke the modal function with the constraint axis configuration and exit.
            self._modal_function(
                "INVOKE_DEFAULT", constraint_axis=constraint_axis)

            return {"FINISHED"}

        return {"PASS_THROUGH"}

    def keypress_phase(self, context: Context, event: Event):
        # Check, if the event is a mouse move.
        if event.type == "MOUSEMOVE":
            # Calculate, how much the mouse was moved in x and y direction.
            delta_x = self._abs(event.mouse_prev_x - event.mouse_x)
            delta_y = self._abs(event.mouse_prev_y - event.mouse_y)

            # Return, if the mouse move was smaller than the sensitivity.
            if delta_x <= self.mouse_pixel_error or delta_y <= self.mouse_pixel_error:
                return {"PASS_THROUGH"}

            # If the mouse was moved, call the modal function and exit.
            self._modal_function("INVOKE_DEFAULT")
            return {"FINISHED"}

        # Check, if the key was released.
        if self._compare_keypress(event, self.key):
            # if self._ignore_event(event):
            # Only listen for RELEASE events.
            if event.value != "RELEASE":
                return {"PASS_THROUGH"}

            print("Hello from the modal operator.")

            # Set the start time for the time window.
            self.start_time = time.time()

            # Set the Operator "phase" to TIME_WINDOW:
            # In this phase, the operator waits for additional keys (as defined in
            # self.other_keys) to be pressed.
            self.phase = "TIME_WINDOW"

            return {"PASS_THROUGH"}

        return {"PASS_THROUGH"}

    def _modal_function(self, *args, **kwargs):
        # Define the function, that will be called as the modal function.
        print(*args, **kwargs)
        # bpy.ops.transform.translate(*args, **kwargs)  # ! DEBUGGING ONLY

    def _gizmo_function(self, *args, **kwargs):
        # Define the function, that will be called as the gizmo function.
        print(*args, **kwargs)
        # bpy.ops.wm.tool_set_by_id(
        # *args, name="builtin.move", **kwargs)  # ! DEBUGGING ONLY

    # #Ignore a keypress event, if the value is not RELEASE.
    # #def _ignore_event(self, keyevent: Event):
    # #    return keyevent.value != "RELEASE"

    # Compare a keypress event with an exact
    # combination of keys (including modifier keys such as crtl, shift, ...)
    def _compare_keypress(self, keyevent: Event, key: str, crtl=False, shift=False, alt=False, oskey=False):
        user_input = [keyevent.type, keyevent.ctrl,
                      keyevent.shift, keyevent.alt, keyevent.oskey]
        wanted_input = [key, crtl, shift, alt, oskey]

        return user_input == wanted_input

    # Return the absolute value of a number.
    def _abs(self, value):
        if value < 0:
            return value * -1

        return value


class GIZMODAL_OPS_OT_move(GIZMODAL_OPS_OT_base):
    """Move selected items"""
    bl_idname = "gizmodal_ops.move"
    bl_label = "Move"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self) -> None:
        super().__init__()
        self.key = "G"

    def _modal_function(self, *args, **kwargs):
        bpy.ops.transform.translate(*args, **kwargs)

    def _gizmo_function(self, *args, **kwargs):
        bpy.ops.wm.tool_set_by_id(*args, name="builtin.move", **kwargs)


class GIZMODAL_OPS_OT_rotate(GIZMODAL_OPS_OT_base):
    """Rotate selected items"""
    bl_idname = "gizmodal_ops.rotate"
    bl_label = "Rotate"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self) -> None:
        super().__init__()
        self.key = "R"

    def _modal_function(self, *args, **kwargs):
        bpy.ops.transform.rotate(*args, **kwargs)

    def _gizmo_function(self, *args, **kwargs):
        bpy.ops.wm.tool_set_by_id(*args, name="builtin.rotate", **kwargs)


class GIZMODAL_OPS_OT_scale(GIZMODAL_OPS_OT_base):
    """Scale selected items"""
    bl_idname = "gizmodal_ops.scale"
    bl_label = "Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self) -> None:
        super().__init__()
        self.key = "S"

    def _modal_function(self, *args, **kwargs):
        bpy.ops.transform.resize(*args, **kwargs)

    def _gizmo_function(self, *args, **kwargs):
        bpy.ops.wm.tool_set_by_id(*args, name="builtin.scale", **kwargs)


keymap = [
    ("transform.translate", GIZMODAL_OPS_OT_move),
    ("transform.rotate", GIZMODAL_OPS_OT_rotate),
    ("transform.resize", GIZMODAL_OPS_OT_scale)
]


def register():
    for _, cls in keymap:
        bpy.utils.register_class(cls)


def unregister():
    for _, cls in reversed(keymap):
        bpy.utils.unregister_class(cls)
