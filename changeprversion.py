#!/usr/bin/python  
# -*- coding=utf-8 -*- 
from xml.etree.ElementTree import ElementTree,Element  
import xml.etree.ElementTree as ET
import os
import sys
import traceback
import time
import gzip

os.system('clear')
print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@ Script written by Hanyuan @ Jul-29-2018 @\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

class Version:
  pass
#setDefault
tgtv = "30"
#targetVersion
tgtvt = "v2015_2"
#targrtVersionDiscrib
      
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
  print '\033[1;35mcurrentVersion is:\033[0m '+child.get("Version")

def show_choices():
  print "\033[1;31;40mWhat version do you want to set?\033[0m\n1) Pr CC 2018.1 -- 35\n2) Pr CC 2018   -- 34\n3) Pr CC 2017.1 -- 33\n4) Pr CC 2017   -- 32\n5) Pr CC 2015.5 -- 31\n6) Pr CC 2015.2 -- 30\n\nq) for quit\n"
  #print "\nWhat version do you want to change?\n1) Pr CC 2018.1\n2) Pr CC 2018\n3) Pr CC 2017.1\n4) Pr CC 2017\n5) Pr CC 2015.5\n6) Pr CC 2015.2\n"

def set_version(inputv,tree):
  global tgtv;
  global tgtvt;
  if inputv == '1':
    tgtv = "35" ;
    tgtvt = "v2018_1";
  elif inputv == '2':
    tgtv = "34" ;
    tgtvt= "v2018";
  elif inputv == '3':
    tgtv = "33" ;
    tgtvt= "v2017_1";
  elif inputv == '4':
    tgtv = "32" ;
    tgtvt= "v2017";
  elif inputv == '5':
    tgtv = "31" ;
    tgtvt= "v2015_5";
  elif inputv == '6':
    tgtv = "30" ;
    tgtvt= "v2015_2";

  num = 0;
  while not tree.findall("Project")[num].get("Version"):
    #找到版本存储位置
      num = num+1;
  else:
    tree.findall("Project")[num].set("Version",tgtv)
    #修改版本为所选值
  return tree




if __name__ == "__main__":

  if len(sys.argv[0:])<2:
    print "\n\033[1;31;40mERROR:\033[0m\nPlease use as $python changeprversion.py \"filepath\"\n";
    exit(0);
    #判断是否输入了文件
  else:
    sourcefile = sys.argv[1]
    #取第2个参数（第一个参数为脚本本身）作为输入文件
    if not os.path.isfile(sourcefile):
      print ('\n\033[1;31;40mError: input file - %s is not exist.\033[0m\nPlease retry.\nGood luck next time.\n' % (sourcefile))
      exit (0);
      #判断文件是否存在，不存在则退出
    try:
      print "\nReading input file:\n"+sourcefile+"\n...";

      zipFile = gzip.open(sourcefile, 'rb')        
      fileContent = zipFile.read();
      sourcefilexml = "/tmp/temp"+str(time.time())+".xml";
      f_tmp = open(sourcefilexml, 'wb')
      f_tmp.write(fileContent);
      f_tmp.close();
      #生成临时文件并将源文件解压得到的xml内容写入

      tree = read_xml(sourcefilexml);
      get_version(tree);
      show_choices();

      inputv = raw_input("Enter your input(eg. 1 for PR CC 2018.1): ");
      while not '0'<inputv<'7':
        if inputv == 'q':
          print "Ok quitting...\nHave a nice day~\n"
          break;
          exit (0);
        else:
          print "Your input: "+inputv+" is not in range 1~6\nPlease input your mind\n"
          inputv = raw_input("Enter your input(eg. 1 for PR CC 2018.1): ");
      #判断输入值是否合法
      else:
        tree = set_version(inputv,tree)
        outfileName=sourcefile.split('.prproj');
        outfileName=outfileName[0]+'_'+tgtvt+'.prproj';
        tree.write("/tmp/out.xml", encoding="utf-8",xml_declaration=True);
        outfileContent = open("/tmp/out.xml");
        outfileContent = outfileContent.read();
        #f_out = open(outfileName+".xml", 'wb');#Debug，直接输出xml不生成prproj
        f_out = gzip.open(outfileName,'wb');
        f_out.write(outfileContent);
        f_out.close();
        zipFile.close()
        #输出prproj文件
        if not os.path.isfile(outfileName):
          print "\033[1;31;40mError: unexcept error.\033[0m\nPlease retry.\nGood luck next time.\n"
        else:
          print "Premiere project Version Changed to "+tgtvt+"\n\033[1;32mNew file saved as:\033[0m"
          print outfileName
          print "\nHave a nice day~\n"
        #判断是否存在输出文件
    except:
      print ('Error: unexcept error.')
      traceback.print_exc()
      zipFile.close()
