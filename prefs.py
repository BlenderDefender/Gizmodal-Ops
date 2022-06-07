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


def layout_preferences(layout: UILayout, prefs):
    # Add a sublayout for all properties that are dependent on auto_lock_to_view.
    numeric_props_col = layout.column()
    numeric_props_col.enabled = not prefs.auto_lock_to_view

    seconds_row = numeric_props_col.row()
    seconds_col = seconds_row.column()

    # Create a row for a label.
    label_row = seconds_col.row()
    label_row.label(
        text="Listen for Modal Operations")
    label_row = seconds_col.row()
    label_row.label(
        text="after pressing G / R / S for:")

    # Display the time_window prop.
    prop_row = seconds_col.row()
    prop_row.alignment = "RIGHT"
    prop_row.label(text="Seconds")
    prop_row.prop(prefs, "time_window", text="")

    # Create a row for a label.
    label_row = numeric_props_col.row()
    label_row.label(
        text="Hold G / R / S + move mouse")
    label_row = numeric_props_col.row()
    label_row.label(
        text="to trigger Lock to View Axis")
    label_row = numeric_props_col.row()
    label_row.label(
        text="Mouse Sensitivity during hold:")

    # Display the mouse_sensitivity prop.
    prop_row = numeric_props_col.row()
    prop_row.alignment = "RIGHT"
    prop_row.label(text="0 - 10")
    prop_row.prop(prefs, "mouse_sensitivity", text="")

    # Create a row for a label.
    label_row = layout.row()
    label_row.label(
        text="Switch to Lock to View Axis")
    label_row = layout.row()
    label_row.label(
        text="when pressing G / R / S")

    prop_row = layout.row()
    prop_row.alignment = "RIGHT"
    prop_row.prop(prefs, "auto_lock_to_view")
    prop_row.label(text="")


class GIZMODAL_OPS_APT_preferences(AddonPreferences):
    bl_idname = __package__

    time_window: FloatProperty(
        name="Time Window",
        description="The time frame, while Gizmodal Ops listens for additional keypresses",
        default=2,
        min=0,
        max=30,
        soft_max=5,
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
            text="then a short time window allows you to press X / Y / Z (etc) for Modal Operations.")
        description_col.label(
            text="Hold G / R / S + move mouse to trigger Lock to View Axis.")


classes = (
    GIZMODAL_OPS_APT_preferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
