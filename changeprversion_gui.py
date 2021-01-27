#!/usr/bin/python  
# -*- coding=utf-8 -*- 
from xml.etree.ElementTree import ElementTree,Element  
import xml.etree.ElementTree as ET
import gzip
import os
import tempfileatexit as tfae
import traceback
import tkinter as tk
from tkinter import filedialog, scrolledtext, END

versiondict = {'0': ('v2020', '38'), '1': ('v2019', '36'), 
        '2': ('v2018_1', '35'), '3': ('v2018', '34'), 
        '4': ('v2017_1', '33'), '5': ('v2017', '32'),
        '6':('v2015_5', '31'), '7':('v2015_2', '30')
        }

rawversiondict = {
        '38': 'Pr CC 2020', 
        '36': 'Pr CC 2019', 
        '35': 'Pr CC 2018.1',
        '34': 'Pr CC 2018',
        '33': 'Pr CC 2017.1',
        '32': 'Pr CC 2017',
        '31': 'Pr CC 2015.5 -- 31',
        '30': 'Pr CC 2015.2'
        }
        
versionlist = ['Pr CC 2020   -- 38', 
        'Pr CC 2019   -- 36', 
        'Pr CC 2018.1 -- 35',
        'Pr CC 2018   -- 34',
        'Pr CC 2017.1 -- 33',
        'Pr CC 2017   -- 32',
        'Pr CC 2015.5 -- 31',
        'Pr CC 2015.2 -- 30'
        ]

def showinfo():
    os.system('cls')
    update_text(text1, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@ Script written by Hanyuan @ Jan-26-2021 @\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")

class Prproj:
    def __init__(self):
        self.path = ""
        self.dir = ""
        self.name = ""
        self.version = ""
        self.tree = None
        #setDefault
        self.tgtv = "30"
        #targetVersion
        self.tgtvt = "v2015_2"

    def readpath(self):
        self.dir, self.name = os.path.split(self.path)

    def readxml(self):
        try:
            zipFile = gzip.open(self.path, mode="rb")        
            fileContent = zipFile.read()
            (fs, sourcefilexml) = tfae.mkstemp()
            f_tmp = open(sourcefilexml, 'wb')
            f_tmp.write(fileContent)
            f_tmp.close()
            zipFile.close()
            #生成临时文件并将源文件解压得到的xml内容写入
            self.tree = read_xmltree(sourcefilexml)
            self.get_version()
        except:
            print('错误: 未知错误.')
            traceback.print_exc()
            zipFile.close()

    def get_version(self):
        root = self.tree.getroot();
        for child in root.findall("Project"):
            if not child.get("Version"):
                continue
        print('原始文件版本号: '+rawversiondict[child.get("Version")]+'\t'+child.get("Version"))
        label1['text'] = '原始文件版本: '+rawversiondict[child.get("Version")]

    def set_version(self):
        if len(list((listbox1.curselection()))) != 0:
            index = str(listbox1.curselection()[0])
            self.tgtv = versiondict[index][1]
            self.tgtvt = versiondict[index][0]
        else:
            update_text(text1, "未选择目标版本\n使用程序默认值: Pr CC 2015.2 -- 30\n")
        num = 0;
        while not projectfile.tree.findall("Project")[num].get("Version"):
            #找到版本存储位置
              num = num+1
        else:
            projectfile.tree.findall("Project")[num].set("Version", self.tgtv)
            #修改版本为所选值
        self.savefile()

    def savefile(self):
        outfileName=self.path.split('.prproj')
        outfileName=outfileName[0]+'_'+self.tgtvt+'.prproj'
        (fs, outxml) = tfae.mkstemp()
        self.tree.write(outxml, encoding="utf-8",xml_declaration=True)
        outfileContent = open(outxml, 'rb')
        outfileContent = outfileContent.read()
        # outfileContent = outfileContent.encode(coding="utf-8")
        # f_out = open(outfileName+".xml", 'wb');#Debug，直接输出xml不生成prproj
        f_out = gzip.open(outfileName,'wb')
        f_out.write(outfileContent)
        f_out.close()
        #输出prproj文件
        if not os.path.isfile(outfileName):
            update_text(text1, "错误: 未知错误.\n请重试.\n祝您好运.\n")
        else:
            update_text(text1, "工程文件已经转换为以下版本: "+self.tgtvt+"\n新文件保存在: \n"+outfileName+"\n祝您一切顺利~\n\n")

def read_xmltree(in_file):
    tree = ElementTree()
    tree.parse(in_file)
    return tree

def openfile():
    projectfile.path = filedialog.askopenfilename(title=u'选择源工程文件').strip()
    filepath.set(projectfile.path)
    if not os.path.isfile(projectfile.path):
      filepath.set('错误: 文件打开失败')
    elif os.path.split(projectfile.path)[1].split('.')[-1] == 'prproj':
        filepath.set(projectfile.path)
        projectfile.readpath()
        label1['text'] ="读取文件中..."
        projectfile.readxml()
    else:
        label1['text'] = "工程文件读取失败"

def update_text(wichtext, input_text):
    print('updating text: ', input_text)
    wichtext.config(state='normal')
    wichtext.insert(END, input_text)
    wichtext.update()
    wichtext.config(state='disabled')

def initgui():
    global filepath
    global text1, label1, listbox1

    window = tk.Tk()
    filepath = tk.StringVar()
    versiontextlist = tk.StringVar()
    versiontextlist.set(versionlist)

    bt1 = tk.Button(text="打开Pr工程文件", font=('TkDefaultFont',18), command=openfile)
    bt1.pack()

    
    ent1 = tk.Entry(textvariable=filepath, font=('TkDefaultFont',18), width=50, state='readonly')
    ent1.pack()

    label1 = tk.Label(font=('TkDefaultFont',18))
    label1.pack()

    label2 = tk.Label(text="转换为哪个版本?", font=('TkDefaultFont',18))
    label2.pack()
    listbox1 = tk.Listbox(listvariable=versiontextlist, font=('TkDefaultFont',18))
    listbox1.pack()
    listbox1.activate(1)

    bt2 = tk.Button(text="开始转换", font=('TkDefaultFont',18), command=projectfile.set_version)
    bt2.pack()

    text1 = scrolledtext.ScrolledText(width=50, height=12, font=('TkDefaultFont',18), fg='black', bg='orange', state='disabled')
    text1.pack()

    showinfo()
    return window


if __name__ == "__main__":
    projectfile = Prproj()

    window = initgui()
    window.title('Pr工程文件版本降级')
    window.mainloop()
