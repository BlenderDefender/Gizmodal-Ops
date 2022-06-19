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
    Panel,
    Context
)


class GIZMODAL_OPS_PT_Panel(Panel):
    """Configure the options for Gizmodal Ops"""
    bl_label = "Gizmodal Ops"
    bl_idname = "GIZMODAL_OPS_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "View"

    def draw(self, context: Context):
        layout = self.layout
        prefs = context.preferences.addons[__package__].preferences

        SPACING = 0.8

        # Add a sublayout for all properties that are dependent on auto_lock_to_view.
        numeric_props_col = layout.column()
        numeric_props_col.enabled = not prefs.auto_lock_to_view

        # Create a row for a label.
        label_col = numeric_props_col.column()
        label_col.scale_y = SPACING
        label_col.label(
            text="Listen for Modal Operations")
        label_col.label(
            text="after pressing G / R / S for:")

        numeric_props_col.separator(factor=1)  # Insert horizontal space.

        # Display the time_window property.
        prop_row = numeric_props_col.row()
        prop_row.alignment = "RIGHT"
        prop_row.label(text="Seconds")
        prop_row.prop(prefs, "time_window", text="")

        numeric_props_col.separator(factor=2.5)  # Insert horizontal space.

        # Create a column for a label.
        label_col = numeric_props_col.column()
        label_col.scale_y = SPACING
        label_col.label(text="────────────────────────")
        label_col.label(
            text="Hold G / R / S + move mouse")
        label_col.label(
            text="to trigger Lock to View Axis")
        label_col.label(text="────────────────────────")

        label_col.separator(factor=SPACING)  # Insert horizontal space.

        label_col.label(
            text="Mouse Sensitivity during hold:")

        numeric_props_col.separator(factor=1)  # Insert horizontal space.

        # Display the mouse_sensitivity property.
        prop_row = numeric_props_col.row()
        prop_row.alignment = "RIGHT"
        prop_row.label(text="0 - 10")
        prop_row.prop(prefs, "mouse_sensitivity", text="")

        numeric_props_col.separator(factor=2.5)  # Insert horizontal space.

        # Create a column for a label.
        label_col = layout.column()
        label_col.scale_y = SPACING
        label_col.label(
            text="Switch to Lock to View Axis")
        label_col.label(
            text="when pressing G / R / S")

        numeric_props_col.separator(factor=1)  # Insert horizontal space.

        # Display the auto_lock_to_view property.
        prop_row = layout.row()
        prop_row.alignment = "RIGHT"
        prop_row.prop(prefs, "auto_lock_to_view")

        # Display a message, when auto save preferences is turned off.
        if not context.preferences.use_preferences_save:
            layout.separator(factor=2.5)  # Insert horizontal space.

            warning_col = layout.column()
            warning_col.enabled = False
            warning_col.scale_y = SPACING
            warning_col.label(text="Remember to save your", icon="ERROR")
            warning_col.label(text="preferences after changing them.")
            warning_col.label(text="Edit > Preferences > Save Preferences")


classes = (
    GIZMODAL_OPS_PT_Panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
