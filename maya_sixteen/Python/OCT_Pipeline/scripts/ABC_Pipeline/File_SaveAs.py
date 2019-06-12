# -*- coding: utf-8 -*-

import maya.cmds as mc
import os,subprocess
import octvDB

class File_SaveAs():
    def __init__(self):
        self.modeDic = {u'rigging': ['_rg', '_msAnim'], u'texture': ['_tx', '_msRender']}

        self.OCTV_TECH = os.getenv('OCTV_TECH') if os.getenv('OCTV_TECH') else '//octvision.com/CG/Tech'
        self.cpauPath = r'%s\bin\CPAU.exe'% os.path.abspath(self.OCTV_TECH)

        self.re_user = r'octvision.com\supermaya'
        self.re_pw = 'supermaya'

    def file_SaveAs(self, fileName, destFolder, mode):
        filePathName = os.path.join(destFolder, fileName)
        filePathName = filePathName.replace('/', '\\')
        masterFilePath =""
        if not os.path.isfile(filePathName):
            print "file not exsit!"
            return False

        newFileName = fileName.replace(self.modeDic[mode][0], self.modeDic[mode][1])

        masterPath = destFolder.replace(mode, "master")
        if newFileName:
            masterFilePath = os.path.join(masterPath, newFileName)
            masterFilePath = masterFilePath.replace('/', '\\')
            bakName = ""
        if os.path.isfile(masterFilePath):
            bakName = self.getBackFile(masterPath, newFileName)

        self.getCopyFile(filePathName, masterFilePath)
        return [newFileName, masterFilePath, bakName]


    # 备份已有的文件
    def getBackFile(self, dirPath, fileName):

        dirBackPath = os.path.join(dirPath, "Backups").replace("\\", "/")
        newfileName = os.path.splitext(fileName)[0]

        listDir = mc.getFileList(fld = dirBackPath, fs = "%s*"% newfileName)

        newNum = ""
        if listDir:
            num = int(sorted(listDir)[-1][-3:]) + 1
            newNum = "%03d" % num
        else:
            newNum = "001"

        bakName = "%s_c%s" % (newfileName, newNum)
        createDirName = os.path.join(dirBackPath, "%s_c%s" % (newfileName, newNum))

        createDirName = createDirName.replace("/", "\\")
        self.getCreateDir(createDirName)

        sourceFile = os.path.join(dirPath, fileName).replace("/", "\\")
        destFile = os.path.join(createDirName, fileName).replace("/", "\\")

        self.getCopyFile(sourceFile, destFile)

        self.delSourceFile(sourceFile)
        return bakName

    #拷贝文件
    def getCopyFile(self, filePathName, masterFilePath):
        cmd = r'%s -u %s -p %s -ex  "COPY /Y  %s %s" -lwp -c -nowarn -wait' % (self.cpauPath, self.re_user, self.re_pw, filePathName, masterFilePath)
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        while True:
            if not p.poll() is None:
                del p
                break

    #创建备份文件夹
    def getCreateDir(self, dirBackPath):
        cmd = r'%s -u %s -p %s -ex  "MD  %s " -lwp -c -nowarn -wait' % (self.cpauPath, self.re_user, self.re_pw, dirBackPath)
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        while True:
            if not p.poll() is None:
                del p
                break

    def delSourceFile(self, filePathName):
        cmd = r'%s -u %s -p %s -ex  "DEL /F /Q  %s " -lwp -c -nowarn -wait' % (self.cpauPath, self.re_user, self.re_pw, filePathName)
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        while True:
            if not p.poll() is None:
                del p
                break


    def insertData(self, db, filename, fstate, ftype, upUser, fpath, checkState, checkUser, desc):
        if db == 'asset' and fstate == 0:
            octvDB.delDB(db, filename)
        octvDB.insertDB(db, filename, fstate, ftype, upUser, fpath, checkState, checkUser, desc)

if __file__== "__main__":
    # fileName = r"JMWC_ch001001character01_l_tx.mb"
    # destFolder = r"//octvision.com/CG/Themes/JMWC/Project/scenes/characters/ch001001character01/texture"
    # mode = r"texture"

    fileName = r"JMWC_ch001001character01_l_rg.mb"
    destFolder = r"//octvision.com/CG/Themes/JMWC/Project/scenes/characters/ch001001character01/rigging"
    mode = r"rigging"

    SaveAsMaster = File_SaveAs()
    infoList = SaveAsMaster.file_SaveAs(fileName, destFolder, mode)

    db = 'asset'
    filename = infoList[0]
    fstate = "0"
    #master模式类型为7
    ftype = "7"
    upUser = os.getenv('username')
    fpath = infoList[1].replace('\\', '/')
    checkState = "1"
    checkUser = ""
    #备注信息
    desc = "test"

    # 插入新文件信息到数据库
    SaveAsMaster.insertData(db, filename, fstate, ftype, upUser, fpath, checkState, checkUser, desc)
    #插入备份信息到数据库
    fstate = "1"
    bakname = infoList[2]
    SaveAsMaster.insertData(db, bakname, fstate, ftype, upUser, fpath, checkState, checkUser, desc)
