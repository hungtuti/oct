# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# '''
# __title__ = '__init__.py'
# __author__ = zhangben
# __mtime__ = 2018/12/5:9:32
# # code is far away from bugs with the god animal protecting
# I love animals. They taste delicious.
# '''
# #
# # __all__ = ['major','minor','ProKits','PCCore']
# #
# # from .ProKits import *
# # from .PCCore import *
# #from . import minor
# # from .major import *
# import sys
# import maya
#
# sys.stdin = maya.app.baseUI.StandardInput()
# # Replace sys.stdout and sys.stderr with versions that can output to Maya's
# # GUI
# sys.stdout = maya.utils.Output()
# sys.stderr = maya.utils.Output( error=1 )

import maya.cmds as mc
import pymel.core as pm
import re,os
import ProKits
import PCCore
import minor
import major