#coding=utf-8
import os,sys,StringIO
from sys import argv
import platform
import shutil
from xml.etree.ElementTree import parse, Element




#cmd
def execCmd(str):
    cmd = str
    r = os.popen(cmd)
    text = r.read()
    buf = StringIO.StringIO(text)
    for line in buf.readlines():
        print (line)
    

#反编译
def decode_apk(str):
	print("Begin to decode_apk...\n")
	execCmd(r"java -jar apktool_2.3.4.jar d %s" %str)
	print( "Zip done!!!")

#和在mf加入 network config
def copy_xml(str):
	print( "Begin copy_xml...\n")
	# execCmd(u"copy /y network_security_config.xml %s\\res\\xml\\" %c)
	shutil.copy('network_security_config.xml', os.path.join(str, 'res', 'xml'))
	print( "Xml is in res/xml!!!")

#插入application
def write_xml(str):
	print( "Begin to insert to application...\n")
	xml_path = parse(os.path.join(str, 'AndroidManifest.xml'))
	root = xml_path.getroot()
	find_appli = root.find('application')
	find_appli.set("ns0:networkSecurityConfig","@xml/network_security_config")
	xml_path.write(os.path.join(str, 'AndroidManifest.xml'))
	print("Insert success!!!")

#回编译
def encode_apk(str):
	print("Begin to encode_apk...\n")
	execCmd(r'java -jar %s b %s -o com.uc.apk' % (os.path.join(os.getcwd(), 'apktool_2.3.4.jar'),str))
	print("Encode done!!!")

#签名
def sign_apk():
	print("Begin to sign_apk...\n") 
	execCmd(r"jarsigner -digestalg SHA1 -sigalg MD5withRSA -verbose -storepass 123456 -keystore uc.keystore -signedjar UC-signed.apk com.uc.apk uctest")
	print("Finally done!!,UC-signed.apk is what you want!!")



def isWindows():
    return platform.system() == "Windows"




def main_run(script,apk_path):
	if not apk_path.endswith('.apk'):
		print('please input apk file full path')
		return

	if not isWindows():
		if '(' in apk_path and ')' in apk_path:
			apk_path = apk_path.replace('(', '\(').replace(')', '\)')

	delete_file = ['com.uc.apk', 'UC-signed.apk']
	for i in delete_file:
		if os.path.exists(i):
			os.remove(i)

	unzip_name = os.path.basename(apk_path)[:-4]
	if os.path.exists(os.path.join(os.getcwd(), unzip_name)):
		if isWindows():
			shutil.rmtree(os.path.join(os.getcwd(), unzip_name))
		else:
			os.popen('rm -fr %s' % os.path.join(os.getcwd(), unzip_name))

	decode_apk(apk_path)

	j = os.path.join(os.getcwd(), unzip_name)

	copy_xml(j)
	write_xml(j)
	encode_apk(j)
	sign_apk()


#主函数
if __name__ == "__main__":
	script_file_path = os.getcwd()
	script,apk_path = argv

	# script, apk_path = '/Users/uc/Desktop/Apk_For_Charles/Apk_For_Charles.py', r'/Users/uc/Desktop/Apk_For_Charles/9appsa.apk'

	main_run(script,apk_path)







