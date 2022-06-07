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


classes = (
    GIZMODAL_OPS_PT_Panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
