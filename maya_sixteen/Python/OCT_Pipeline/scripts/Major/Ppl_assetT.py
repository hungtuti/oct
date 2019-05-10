#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = Ppl_checkT_asset
__author__ = zhangben 
__mtime__ = 2019/4/1 : 18:24
# code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
"""
import shutil
from PySide import QtGui,QtCore,QtUiTools
import maya.OpenMayaUI as mui
import sys,os,copy,re
import maya.mel as mel
import maya.cmds as mc
import pymel.core as pm
import shiboken
from ..utility import Kits
reload(Kits)
from ..past import sk_checkTools,sk_sceneTools,sk_smoothSet
reload(sk_checkTools)
reload(sk_sceneTools)
reload(sk_smoothSet)
SCRIPT_LOC = os.path.split(__file__)[0]
PROJ_DIR = os.getenv('OCTV_PROJECTS')
class Ppl_assetT_main(QtGui.QMainWindow):
    def __init__(self):#load ui  show it
        """
        前期检测整理工具集
        """
        ppl_UI = os.path.join(Kits.Kits.get_dir(SCRIPT_LOC, 2), r'media\ppl_assetTool.ui')
        MayaMain = shiboken.wrapInstance(long(mui.MQtUtil.mainWindow()), QtGui.QWidget)
        super(Ppl_assetT_main,self).__init__(MayaMain)
        #=======program MEL path ====================
        self.mel_dir = os.path.join(Kits.Kits.get_dir(SCRIPT_LOC, 1),'MEL')
        #=======relative modules======================
        self.skchk = sk_checkTools.sk_checkTools()
        self.sksct = sk_sceneTools.sk_sceneTools()
        self.sksmth = sk_smoothSet.sk_smoothSet()
        # main window load/settings
        self.ui = self.loadUiWidget(ppl_UI,MayaMain)
        self.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose,True)
        self.ui.destroyed.connect(self.cmd_onExitCode)
        self.ui.move(200,400)
        self.buttonsList = [ea_bt.objectName() for ea_bt in self.ui.findChildren(QtGui.QPushButton) if ea_bt.objectName().endswith('_bt')]

        self.ui.show()

        self.makeConnections()
        # === about porjects information
        self.k = Kits.Kits()
        ALL_PROJ_ABBRS = os.listdir(PROJ_DIR)
        sc_shn = os.path.basename(pm.sceneName())
        self.proj_abbr = re.search("^[^_]+",sc_shn).group() if sc_shn and re.search("^[^_]+",sc_shn).group() != sc_shn else None



    def makeConnections(self): # connect buttons to fucntions
        for each_bt in self.buttonsList:
            _fuction = getattr(self,"cmd_{}".format(each_bt)) if "cmd_{}".format(each_bt) in self.__class__.__dict__ else self._somFunc
            self.ui.findChildren(QtGui.QPushButton, each_bt)[0].clicked.connect(_fuction)
    #=========↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓   connected functions ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓========================================
    def cmd_onExitCode(self):
        sys.stdout.write("You closed the demo ui !!\n")
    def _somFunc(self):
        print("some function return what a F~~")
    #  call tools buttons commands =================================
    def cmd_rnmT_bt(self):#重命名工具
        src_mel = os.path.abspath(os.path.join(self.mel_dir, 'Quick_rename_tool.mel'))
        src_mel = re.sub(r'\\','/',src_mel)
        mel.eval("source \"{}\"".format(src_mel))
        mel.eval("Quick_rename_tool()")

    def cmd_alterTxsPrf_bt(self):#修改贴图前缀匹配当前项目
        mod = {'RENAME OLD':'rn','COPIED FOR NEW':'cp'}
        result = mc.promptDialog(title='Texture Prefix',message='Enter Prefix:',button=['COPIED FOR NEW','RENAME OLD','Cancel'],defaultButton='OK',
                                 cancelButton='Cancel',
                                 dismissString='Cancel',text = self.proj_abbr)
        if result in mod: self.proj_abbr = mc.promptDialog(query=True, text=True)
        else:return
        ALL_PROJ_ABBRS = os.listdir(PROJ_DIR)
        alterFs = pm.selected(type='file')
        if not alterFs: alterFs = pm.ls(type='file')
        cur_proj_wsp = pm.workspace(fn=True, q=True)
        cur_src_dir = "{}/sourceimages/".format(cur_proj_wsp)
        all_cnt = len(alterFs)
        renmed_txs_cnt = 0
        prg_num = (renmed_txs_cnt+1 / float(all_cnt)) * 100
        cpProgressWin = mc.progressWindow(title="Add Prefix", progress=prg_num, status="PROGRESS : {}%".format(prg_num), isInterruptable=True,
                                          min=0, max=100)
        for eaf in alterFs:
            get_txfpths = []
            txfpth_01 = eaf.attr('fileTextureName').get()
            get_txfpths.append(txfpth_01)
            if self.get_ArTx(txfpth_01) and os.path.isfile(self.get_ArTx(txfpth_01)): get_txfpths.append(self.get_ArTx(txfpth_01))
            for txfpth in get_txfpths:
                set_attr_value = True
                if get_txfpths.index(txfpth): set_attr_value = False
                txf_nm = os.path.basename(txfpth)
                txf_prj_abbr = re.search("^[^_]+", txf_nm).group()
                if txf_prj_abbr == self.proj_abbr: continue
                txf_dir = re.sub(txf_nm, '', txfpth)
                print txf_dir
                if not txf_dir == cur_src_dir and mod[result]=='cp':
                    txf_dir = cur_src_dir
                new_txf_nm = None
                if txf_prj_abbr in ALL_PROJ_ABBRS:
                    new_txf_nm = re.sub(txf_prj_abbr, self.proj_abbr, txf_nm)
                else : new_txf_nm = '{}_{}'.format(self.proj_abbr,txf_nm)
                new_txf_pth = "{}{}".format(txf_dir, new_txf_nm)
                if self.k.filetest(txfpth,new_txf_pth):
                    # print(">>>--{}{}>>>---{}".format(txfpth,os.linesep,new_txf_pth))
                    try:
                        if mod[result] =='cp':
                            shutil.copy2(txfpth,new_txf_pth)
                            if set_attr_value:
                                eaf.attr('fileTextureName').set(new_txf_pth)
                        elif mod[result] =='rn':
                            eaf.attr('fileTextureName').set("")
                            os.rename(txfpth,new_txf_pth)
                            if set_attr_value:
                                eaf.attr('fileTextureName').set(new_txf_pth)
                        renmed_txs_cnt +=1
                        self.ref_pr_bar(renmed_txs_cnt+1,all_cnt,cpProgressWin)
                    except:
                        print("sorce image: {1}{0}target image: {2}".format(os.linesep,txfpth,new_txf_pth))
                        mc.progressWindow(cpProgressWin, endProgress=1)
                        print(u">>>请检查 当前工程的sourceimages文件夹 是否存在并且有写入权限")
                        mc.error(u'{0}>>>请检查 当前工程的sourceimages文件夹 是否存在并且有写入权限{0}\t{1}'.format(os.linesep,txf_dir))
                else:
                    if os.path.exists(new_txf_pth):
                        eaf.attr('fileTextureName').set(new_txf_pth)
                        renmed_txs_cnt += 1
                        self.ref_pr_bar(renmed_txs_cnt + 1, all_cnt, cpProgressWin)
        mc.progressWindow(cpProgressWin, endProgress=1)
        print(u">>> 本次操作修改了 {} 张贴图前缀 匹配了当前文件 项目 缩写 : {} ".format(renmed_txs_cnt,self.proj_abbr))


    def cmd_smoothSetT_bt(self): # smooth set 设置工具
        self.sksmth.UI_setSmooth()
    #  call fuction buttons commands ================================
    # 根据名字选择
    def cmd_selByNm_bt(self):
        srcStr = self.ui.pick_sel_l.text()
        ls_objs = pm.ls(srcStr)
        pm.select(ls_objs)
    # 自动重命名
    def cmd_nm_tidy_bt(self):
        from ..Minor import Ppl_rnmtools_auto
        reload(Ppl_rnmtools_auto)
        Ppl_rnmtools_auto.Pre_regNaming()
    # 添加后缀 _
    def cmd_suff_tidy_bt(self):
        self.skchk.checkRenameMSHPosfix()
    # 检查 namespace
    def cmd_chkNmsp(self):
        self.skchk.checkModelDetailsWarning("nsCheck")
    # namespace工具
    def cmd_nmsp_tidy_bt(self):
        src_mel = os.path.abspath(os.path.join(self.mel_dir,'common_namespaceTools.mel'))
        src_mel = re.sub(r'\\', '/', src_mel)
        mel.eval("source \"{}\"".format(src_mel))
        mel.eval("common_namespaceTools")
    # 清理多余的显示层
    def cmd_dsly_tidy_bt(self):
        self.sksct.checkCleanDisplayLayers()
        print("DisplayLayer Tidied!!!")
    # delete empty group
    def cmd_emgrp_tidy_bt(self):
        allTrans = pm.ls(tr=True)
        emt = []
        for e in allTrans:
            print e
    #添加 ct_an 标记 标记物体输出动画
    def cmd_anlab_tidy_bt(self):
        self.skchk.checkCTANSignAdd()
    def cmd_set_tidy_bt(self):# 自动标记set组
        self.sksct.checkCacheSetAdd()
        self.sksct.checkTransAnimSetAdd()
        self.sksct.sk_sceneCacheAnimSetConfig("Cache", "ZM")
        self.sksct.sk_sceneCacheAnimSetConfig("Anim", "ZM")
    def cmd_ref_chk_bt(self):#检查参考
        self.skchk.checkModelDetailsWarning("refCheck")
    def cmd_nmsp_chk_bt(self):#检查namespace
        self.skchk.checkModelDetailsWarning("nsCheck")
    def cmd_nm_chk_bt(self):#检查命名
        self.skchk.checkModelDetailsWarning("MSHCheck")
    def cmd_fnm_chk_bt(self):#检查面数
        self.skchk.checkModelDetailsWarning("faceCheck")
    def cmd_ins_chk_bt(self):#检查instance
        self.skchk.checkModelDetailsWarning("insCheck")
    def cmd_sm_chk_bt(self):  # 检查smooth
        self.skchk.checkModelDetailsWarning("moothCheck")
    def cmd_flg_chk_bt(self):  # 检测属性标记
        self.skchk.checkModelDetailsWarning("signCheck")
    def cmd_tautonymy_chk_bt(self):  # 检查 transform 同名
        self.skchk.checkModelDetailsWarning("sameTransformCheck")
    def cmd_tautonymyShp_chk_bt(self): # 检查 shape同名
        self.skchk.checkModelDetailsWarning("sameShapeCheck")
    def cmd_tautonymyMsh_chk_bt(self): # 检查 mesh 同名
        self.skchk.checkModelDetailsWarning("sameShapeNodeCheck")
    def cmd_smthSet_chk_bt(self): # 检查smooth set
        self.skchk.checkModelDetailsWarning("smoothSet")
    def cmd_prxTr_chk_bt(self): # 检查proxy 位移
        self.skchk.checkModelDetailsWarning("proxyInfo")
    def cmd_rndSta_chk_bt(self):#检查 render state
        self.skchk.checkModelDetailsWarning("renderState")
    def cmd_selSmth_tidy_bt(self):#选取物体smooth
        self.sksmth.smoothSetDoSmooth(useSmoothSet = 1,selMode = 1)
    def cmd_txsnm_chk_bt(self):#check 贴图命名
        chk_labels = {'noExists': u'贴图不存在', 'iffyName': u'贴图命名 应由 (字母/数字/_/.) 组成', 'seqIffyName': u'序列贴图序号存在异常 正常为 ***.0001.jpg', 'prefIffyName':
            u'贴图前缀与当前任务不匹配'}
        res = self.chk_txf_name()
        res_str = u'>>>请检查列出的file节点 贴图命名 所描述的错误{}'.format(os.linesep)
        ck_cnt = 0
        for ea_ck_lb in chk_labels:
            if res[ea_ck_lb]:
                res_str += u'\t{}{}'.format(chk_labels[ea_ck_lb], os.linesep)
                for ea_fn in res[ea_ck_lb]:
                    res_str += u"\t\t>>>File Node >> {:<32}\t>>>Texture File>>  {:<120}\t 异常部分: {}{}".format(ea_fn.name(), res[ea_ck_lb][
                        ea_fn].keys()[
                        0],res[ea_ck_lb][ea_fn].values()[0], os.linesep)
                ck_cnt +=1
        if ck_cnt: print res_str
        else: print(u">>>没有贴图节点被check")


    # check all items
    def cmd_all_chk_bt(self):
        print("\n".join(self.buttonsList))


    # smoothSetDoSmooth(useSmoothSet = 1,selMode = 1)

    #=========↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑    connected functions  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑========================================

    def loadUiWidget(self,uifilename, parent=None): # load ui file
        """import ui file"""
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(uifilename)
        uifile.open(QtCore.QFile.ReadOnly)
        ui = loader.load(uifile, parent)
        uifile.close()
        return ui


    def nonUniqueObjects(self): # a function list all taotunymy object
        all_nds = pm.ls()
        non_uniques = {}
        temp_nm_dic = {}
        for ea_nd in all_nds:
            ndTyp = ea_nd.type()
            ndShtNm = ea_nd.name()
            ndLngNm = ea_nd.longName()
            if ndShtNm not in temp_nm_dic:
                temp_nm_dic[ndShtNm] = {ndTyp: [ea_nd]}
            else:
                if ndShtNm not in non_uniques:
                    cp_date = copy.deepcopy(temp_nm_dic[ndShtNm])
                    non_uniques[ndShtNm] = cp_date
                    if ndTyp in non_uniques[ndShtNm]:
                        non_uniques[ndShtNm].append(ea_nd)
                    else:
                        non_uniques[ndShtNm][ndTyp] = [ea_nd]
                else:
                    if ndTyp in non_uniques[ndShtNm]:
                        non_uniques[ndShtNm].append(ea_nd)
                    else:
                        non_uniques[ndShtNm][ndTyp] = [ea_nd]

    def chk_txf_name(self,proj_abbr=None):  # texture file name check
        if not proj_abbr:  # project abbreviation
            fileName_shn = mc.file(q=True, sn=True, shn=True)
            proj_abbr = re.search('^[^_]*', fileName_shn).group()
            if proj_abbr == fileName_shn: proj_abbr == None
        lsfils = pm.ls(type='file')
        checkRes = {'noExists': {}, 'iffyName': {}, 'seqIffyName': {}, 'prefIffyName': {}}
        for eaf in lsfils:
            txfpth = eaf.attr('fileTextureName').get()
            txf_nm = os.path.basename(txfpth)
            txf_prf = re.search("^[^_]+", txf_nm).group()
            # check texture file prefix match project abbreviation
            if proj_abbr and proj_abbr != txf_prf:
                checkRes['prefIffyName'][eaf] = {txfpth:txf_prf}
            # check file whether exists
            if not os.path.isfile(txfpth): checkRes['noExists'][eaf] = [txfpth]
            # check file name whether
            re_iffynm = re.compile("[^\w_/{}:.]+".format(os.sep), re.I)
            ckres = re_iffynm.findall(txfpth)
            if len(ckres): checkRes['iffyName'][eaf] = {txfpth: ckres}
            # check sequence texture
            if eaf.attr('useFrameExtension').get() or eaf.attr('uvTilingMode').get() == 3:
                tx_spl = os.path.splitext(txf_nm)
                re_seq = re.compile('[._]+\d+$', re.I)
                if not re_seq.search(tx_spl[0]):
                    re_seq_comp = re.compile('[^_.]+$', re.I)
                    if re_seq_comp.search(tx_spl[0]):
                        checkRes['seqIffyName'][eaf] = {txfpth: re_seq_comp.findall(tx_spl[0])}
                    else:
                        checkRes['seqIffyName'][eaf] = {txfpth: [tx_spl[0]]}
                else:
                    match_seq = re_seq.search(tx_spl[0]).group()
                    print match_seq
                    re_illegal_seq = re.compile('[._]')
                    redundant_sep = re_illegal_seq.findall(match_seq)[:-1]
                    if redundant_sep: checkRes['seqIffyName'][eaf] = {txfpth: redundant_sep}
        return checkRes

    def ref_pr_bar(self,cur_cp_num, exec_count, cpProgressWin):# 更新进度条
        prg_num_tmp = (cur_cp_num / float(exec_count)) * 100
        mc.progressWindow(cpProgressWin, e=True, progress=prg_num_tmp, status="Copy perform: {}%".format(prg_num_tmp))

    def get_ArTx(self,src):#把arnold tx文件加入copy列表
        if not mc.getAttr("defaultRenderGlobals.currentRenderer") =="arnold": return None
        fileSpl = os.path.splitext(src)
        txf_pth = fileSpl[0] + u'.tx'
        if txf_pth == src:return None
        else: return txf_pth


# def call_it():
#     if not mc.window('ppl_asset_win',exists=True):
#         win = Ppl_assetT_main()
#     else:
#         sys.stdout.write("Tools is already open!\n")

    #win.showUI()