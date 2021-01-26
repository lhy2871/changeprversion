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
    os.system('clear')
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
  print('Current version is: '+child.get("Version"))

def show_choices():
  print("What version do you want to set?\n \
        1) Pr CC 2020   -- 38\n \
        2) Pr CC 2019   -- 36\n \
        3) Pr CC 2018.1 -- 35\n \
        4) Pr CC 2018   -- 34\n \
        5) Pr CC 2017.1 -- 33\n \
        6) Pr CC 2017   -- 32\n \
        7) Pr CC 2015.5 -- 31\n \
        8) Pr CC 2015.2 -- 30\n\n \
        q) for quit\n")
  #print "\nWhat version do you want to change?\n1) Pr CC 2018.1\n2) Pr CC 2018\n3) Pr CC 2017.1\n4) Pr CC 2017\n5) Pr CC 2015.5\n6) Pr CC 2015.2\n"

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
    sourcefile = input("请打开要处理的pr工程文件: ").strip()
    if not os.path.isfile(sourcefile):
      print ('Error: input file - %s is not exist.\nPlease retry.\nGood luck next time.\n' % (sourcefile))
      quit()
      #判断文件是否存在，不存在则退出
    try:
      print("Reading input file...")
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

      inputv = input("Enter your input(eg. 1 for PR CC 2020): ");
      while not '0'<inputv<'7':
        if inputv == 'q':
          print("Ok quitting...\nHave a nice day~\n")
          break;
          exit (0);
        else:
          print("Your input: "+inputv+" is not in range 1~6\nPlease input your mind\n")
          inputv = input("Enter your input(eg. 1 for PR CC 2020): ");
      #判断输入值是否合法
      else:
        tree, tgtvt = set_version(inputv,tree)
        outfileName=sourcefile.split('.prproj')
        outfileName=outfileName[0]+'_'+tgtvt+'.prproj'
        (fs, outxml) = tfae.mkstemp()
        tree.write(outxml, encoding="utf-8",xml_declaration=True);
        outfileContent = open(outxml);
        outfileContent = outfileContent.read();
        outfileContent = outfileContent.encode()
        #f_out = open(outfileName+".xml", 'wb');#Debug，直接输出xml不生成prproj
        f_out = gzip.open(outfileName,'wb');
        f_out.write(outfileContent);
        f_out.close();
        zipFile.close()
        #输出prproj文件
        if not os.path.isfile(outfileName):
          print("Error: unexcept error.\nPlease retry.\nGood luck next time.\n")
        else:
          print("Premiere project Version Changed to "+tgtvt+"\nNew file saved as:")
          print(outfileName)
          print("\nHave a nice day~\n")
        #判断是否存在输出文件
    except:
      print('Error: unexcept error.')
      traceback.print_exc()
      zipFile.close()
