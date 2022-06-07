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

from .prefs import layout_preferences


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

        layout_preferences(layout, prefs)


classes = (
    GIZMODAL_OPS_PT_Panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
