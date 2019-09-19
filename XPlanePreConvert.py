#!BPY
""" Registration info for Blender menus:
Name: 'X-Plane Pre-Conversion Fixes'
Blender: 249
Group: 'Misc'
Tooltip: 'Generate scripts that allow the 2.49 converter to fix certain forward compatibility bugs'
"""
__author__ = 'Theodore "Ted" Greene'
__email__ = "<ted at x-plane dot com>"
__url__ = "XPlane2Blender, https://github.com/X-Plane/XPlane2Blender"
__version__ = "1.0"
__bpydoc__ = """\
Generates scripts for the 2.49 converter to use
after loading the .blend file in Blender 2.79.

This script only creates text files, not the actual changes

Creates the following scripts

- FixDroppedActions.py

Generated scripts can be edited before put through the converter
and can be deleted after conversion.
"""

#------------------------------------------------------------------------
#
# Copyright (c) 2019 Theodore "Ted" Greene
#
# Mail: <ted@x-plane.com>
# Web:  https://github.com/X-Plane/XPlane2Blender
#
# This software is licensed under a Creative Commons License
#   Attribution-Noncommercial-Share Alike 3.0:
#
#   You are free:
#   * to Share - to copy, distribute and transmit the work
#   * to Remix - to adapt the work
#
#   Under the following conditions:
#   * Attribution. You must attribute the work in the manner specified
#     by the author or licensor (but not in any way that suggests that
#     they endorse you or your use of the work).
#   * Noncommercial. You may not use this work for commercial purposes.
#   * Share Alike. If you alter, transform, or build upon this work,
#     you may distribute the resulting work only under the same or
#     similar license to this one.
#
#   For any reuse or distribution, you must make clear to others the
#   license terms of this work.
#
# This is a human-readable summary of the Legal Code (the full license):
#   http://creativecommons.org/licenses/by-nc-sa/3.0/

import collections

import Blender
from Blender import Text

def make_dropped_actions_script():
    actions_and_users = collections.defaultdict(list) # type: Dict[ActionName, List[ObjectName]]
    for scene in Blender.Scene.Get():
        # Techinically the bug is just "all after the first
        # encountered object, alphabetically"
        # but including everything makes for better bug reports
        for obj in reversed(scene.objects):
            action = obj.getAction()
            if action:
                actions_and_users[action.getName()].append(obj.getName())

    actions_and_users = dict([(action, users) for action, users in actions_and_users.items() if len(users) > 1])

    if not actions_and_users:
        return
    else:
        script = (
            "# Must contain a non-empty Python Dict"
            " where Key=Action name, Value=List[Name of Object that uses said Action]\n"
            + "{\n"
                + ",\n".join("    '%s':%s"%(action, str(users)) for action, users in actions_and_users.items())
            + "\n}"
        )

        dropped_actions_script_name = "FixDroppedActions.py"

        try:
            dropped_actions_script = Blender.Text.Get(dropped_actions_script_name)
        except NameError:
            dropped_actions_script = Blender.Text.New(dropped_actions_script_name)
        finally:
            dropped_actions_script.clear()
            for line in script.split("\n"):
                dropped_actions_script.write(line + "\n")

# Alternatively, you can comment these lines to prevent the generation of
# text blocks (this won't delete existing ones, however)
make_dropped_actions_script()