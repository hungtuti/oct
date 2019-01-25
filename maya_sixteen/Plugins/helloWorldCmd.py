"""
To use, make sure that helloWorldCmd.py is in your MAYA_PLUG_IN_PATH (and the
C++ version is not) then do the following:

import maya.cmds
maya.cmds.loadPlugin("helloWorldCmd.py")
maya.cmds.spHelloWorld()
"""

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

# command
class HelloWorldCmd(OpenMayaMPx.MPxCommand):
	kPluginCmdName = "spHelloWorld"

	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)

	@staticmethod
	def cmdCreator():
		return OpenMayaMPx.asMPxPtr( HelloWorldCmd() )

	def doIt(self,argList):
		print "Hello World!"


# Initialize the script plug-in
def initializePlugin(plugin):
	pluginFn = OpenMayaMPx.MFnPlugin(plugin)
	try:
		pluginFn.registerCommand(
			HelloWorldCmd.kPluginCmdName, HelloWorldCmd.cmdCreator
		)
	except:
		sys.stderr.write(
			"Failed to register command: %s\n" % HelloWorldCmd.kPluginCmdName
		)
		raise

# Uninitialize the script plug-in
def uninitializePlugin(plugin):
	pluginFn = OpenMayaMPx.MFnPlugin(plugin)
	try:
		pluginFn.deregisterCommand(HelloWorldCmd.kPluginCmdName)
	except:
		sys.stderr.write(
			"Failed to unregister command: %s\n" % HelloWorldCmd.kPluginCmdName
		)
		raise

#-
# ==========================================================================
# Copyright (C) 2011 Autodesk, Inc. and/or its licensors.  All
# rights reserved.
#
# The coded instructions, statements, computer programs, and/or related
# material (collectively the "Data") in these files contain unpublished
# information proprietary to Autodesk, Inc. ("Autodesk") and/or its
# licensors, which is protected by U.S. and Canadian federal copyright
# law and by international treaties.
#
# The Data is provided for use exclusively by You. You have the right
# to use, modify, and incorporate this Data into other products for
# purposes authorized by the Autodesk software license agreement,
# without fee.
#
# The copyright notices in the Software and this entire statement,
# including the above license grant, this restriction and the
# following disclaimer, must be included in all copies of the
# Software, in whole or in part, and all derivative works of
# the Software, unless such copies or derivative works are solely
# in the form of machine-executable object code generated by a
# source language processor.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# AUTODESK DOES NOT MAKE AND HEREBY DISCLAIMS ANY EXPRESS OR IMPLIED
# WARRANTIES INCLUDING, BUT NOT LIMITED TO, THE WARRANTIES OF
# NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR
# PURPOSE, OR ARISING FROM A COURSE OF DEALING, USAGE, OR
# TRADE PRACTICE. IN NO EVENT WILL AUTODESK AND/OR ITS LICENSORS
# BE LIABLE FOR ANY LOST REVENUES, DATA, OR PROFITS, OR SPECIAL,
# DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES, EVEN IF AUTODESK
# AND/OR ITS LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY
# OR PROBABILITY OF SUCH DAMAGES.
#
# ==========================================================================
#+
