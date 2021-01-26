#!/usr/bin/python  
# -*- coding=utf-8 -*- 
from xml.etree.ElementTree import ElementTree,Element  
import xml.etree.ElementTree as ET
import gzip
import os
import tempfileatexit as tfae
import traceback

versiondict = {'1': ('2020', '38'), '2': ('2019', '36'), 
        '3': ('2018.1', '35'), '4': ('2018', '34'), 
        '5': ('2017.1', '33'), '6': ('2017', '32'),
        '7':('2015.5', '31'), '8':('2015.2', '30')
        }

def showinfo():
    os.system('cls')
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@ Script written by Hanyuan @ Jan-26-2021 @\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

class Version:
  pass
      
def read_xml(in_file):  
  '''''读取并解析xml文件 
    in_path: xml路径 
    return: ElementTree'''  
  tree = ElementTree()  
  tree.parse(in_file)  
  return tree
  
def get_version(tree):
  root = tree.getroot();
  for child in root.findall("Project"):
    if not child.get("Version"):
      continue
  print('原始文件版本号: '+child.get("Version"))

def show_choices():
  print("转换为哪个版本?\n \
        1) Pr CC 2020   -- 38\n \
        2) Pr CC 2019   -- 36\n \
        3) Pr CC 2018.1 -- 35\n \
        4) Pr CC 2018   -- 34\n \
        5) Pr CC 2017.1 -- 33\n \
        6) Pr CC 2017   -- 32\n \
        7) Pr CC 2015.5 -- 31\n \
        8) Pr CC 2015.2 -- 30\n\n \
        q) 退出程序\n")

def set_version(inputv,tree):
    #setDefault
    tgtv = "30"
    #targetVersion
    tgtvt = "v2015_2"
    tgtv = versiondict[inputv][1]
    tgtvt = versiondict[inputv][0]

    num = 0;
    while not tree.findall("Project")[num].get("Version"):
        #找到版本存储位置
          num = num+1
    else:
        tree.findall("Project")[num].set("Version",tgtv)
        #修改版本为所选值
    return tree, tgtvt


if __name__ == "__main__":
    showinfo()
    sourcefile = input("请打开(把文件拖到此窗口)要处理的pr工程文件: ").strip()
    if not os.path.isfile(sourcefile):
      print ('错误: 指定的文件 - %s 不存在.\n请重试.\n祝您好运.\n' % (sourcefile))
      os.system('pause')
      quit()
      #判断文件是否存在，不存在则退出
    try:
      print("读取文件中...")
      zipFile = gzip.open(sourcefile, 'rb')        
      fileContent = zipFile.read()
      # sourcefilexml = "/tmp/temp"+str(time.time())+".xml"
      (fs, sourcefilexml) = tfae.mkstemp()
      f_tmp = open(sourcefilexml, 'wb')
      f_tmp.write(fileContent);
      f_tmp.close();
      #生成临时文件并将源文件解压得到的xml内容写入

      tree = read_xml(sourcefilexml)
      # tree = read_xml(fileContent)
      get_version(tree)
      show_choices()

      inputv = input("请输入(例如: 1 意味着转换成Pr CC 2020): ");
      while not '0'<inputv<'9':
        if inputv == 'q':
          print("正在退出...\n祝您一切顺利~\n")
          break;
          os.system('pause')
          quit(0);
        else:
          print("你输入的: "+inputv+"\n不在 1~8 范围内\n请重新输入\n")
          inputv = input("请输入(例如: 1 意味着转换成Pr CC 2020): ");
      #判断输入值是否合法
      else:
        tree, tgtvt = set_version(inputv,tree)
        outfileName=sourcefile.split('.prproj')
        outfileName=outfileName[0]+'_'+tgtvt+'.prproj'
        (fs, outxml) = tfae.mkstemp()
        tree.write(outxml, encoding="utf-8",xml_declaration=True);
        outfileContent = open(outxml, 'rb');
        outfileContent = outfileContent.read();
        # outfileContent = outfileContent.encode(coding="utf-8")
        #f_out = open(outfileName+".xml", 'wb');#Debug，直接输出xml不生成prproj
        f_out = gzip.open(outfileName,'wb');
        f_out.write(outfileContent);
        f_out.close();
        zipFile.close()
        #输出prproj文件
        if not os.path.isfile(outfileName):
          print("错误: 未知错误.\n请重试.\n祝您好运.\n")
        else:
          print("工程文件已经转换为以下版本: "+tgtvt+"\n新文件保存在:")
          print(outfileName)
          print("\n祝您一切顺利~\n")
          os.system('pause')
        #判断是否存在输出文件
    except:
      print('错误: 未知错误.')
      traceback.print_exc()
      zipFile.close()
      os.system('pause')
      