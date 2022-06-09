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
    AddonPreferences,
    Context,
    UILayout
)

from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
)


class GIZMODAL_OPS_APT_preferences(AddonPreferences):
    bl_idname = __package__

    time_window: FloatProperty(
        name="Time Window",
        description="The time frame, while Gizmodal Ops listens for additional keypresses",
        default=2,
        max=5,
        min=1,
        precision=1,
        subtype="TIME"  # IDEA: TIME_ABSOLUTE is a thing since 3.0
    )

    mouse_sensitivity: IntProperty(
        name="Mouse sensitivity",
        description="How sensitive Gizmodal Ops should react to mouse moves.",
        default=10,
        min=0,
        max=10
    )

    auto_lock_to_view: BoolProperty(
        name="Auto",
        description="Automatically switch to Lock to view Axis when pressing G / R / S.",
        default=False
    )

    def draw(self, context: Context):

        layout: UILayout = self.layout

        # Add a sublayout for the addon description.
        description_col = layout.column()
        description_col.scale_y = 0.8

        # Addon description
        description_col.label(text="Press G / R / S to show the Gizmo,")
        description_col.label(
            text="then a short time window allows you to activate Modal Operations")
        description_col.label(text="by pressing X / Y / Z (etc).")
        description_col.separator(factor=2.5)

        description_col.label(
            text="Hold G / R / S + move mouse to activate Lock to View Axis.")

        description_col.separator(factor=7.5)
        description_col.label(
            text="Supports default Blender keymap. Compatibility with other keymaps will vary.", icon="ERROR")


classes = (
    GIZMODAL_OPS_APT_preferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
