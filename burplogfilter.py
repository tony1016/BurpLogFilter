#!/usr/bin/env python3
#coding=utf-8
import getopt
import sys
import re

DEBUG=False
url_param_patterns=[];

def main():
    global DEBUG

    try:
        options,args = getopt.getopt(sys.argv[1:],"f:hv",["host="])
    except getopt.GetoptError:
        print("[WARNING] error, to see help message of options run with '-h'")
        sys.exit()

    if ('-v', '') in options:
        DEBUG=True

    filename=None
    host=None

    for opt,arg in options:
        if opt == "-f":
            filename=arg.strip("'")
        if opt == "--host":
            host=arg.strip("'")
        if opt == "-h":
            showHelp()
            return

    blocks=scrapBlocks(filename)
    filteredBlocks=[]
    for block in blocks:
        if isBlockUseful(block,host) :
            filteredBlocks.append(block)

    for block in filteredBlocks:
        outputBlock(block)

def scrapBlocks(filename):
    global DEBUG

    if DEBUG:
        print("Try to anayze file %s"%filename)

    blocks=None
    with open(filename, 'rb') as f:
        content=f.read()
        blocks = re.findall(r'======================================================'
            r'.*?======================================================'
            r'.*?======================================================', content, re.S)
        if DEBUG:
            print("The file contains %s block(s)"%len(blocks))

    return blocks
    

def isBlockUseful(block,host,isFilterStaticResource=True):
    global url_param_patterns

    # 过滤静态资源
    for line in block.split("\n"):
        if re.match("^GET",line):
            if isFilterStaticResource and line.split(" ")[1].split("?")[0].split(".")[-1] in (("bmp","bz2","css","doc","eot","flv","gif","gz","ico","jpeg","jpg","js","less","mp[34]","pdf","png","rar","rtf","swf","tar","tgz","txt","wav","woff","xml","zip")):
                if DEBUG:
                    print("[DEBUG] Filter this static resource url %s"%line.split(" ")[1])
                return False

    # 过滤Host
    if host:
        for line in block.split("\n"):
            m = re.match(r"^Host:(.*)", line)
            if m and host not in m.group(1).strip():
                if DEBUG:
                    print("[DEBUG] Filter this host %s" % m.group(1).strip())
                return False

    # 过滤URL模式
    for line in block.split("\n"):
        if re.match("^GET",line) or re.match("^POST",line):
            url=line.split(" ")[1].split("?")[0]
            params=""
            if "?" in line:
                params=line.split(" ")[1].split("?")[1]
            

            pattern=generatePattern(line.split(" ")[0],url,params)
            if pattern in url_param_patterns:
                if DEBUG:
                    print("[DEBUG] Pattern %s exists"%pattern)
                return False
            else:
                url_param_patterns.append(pattern)
                if DEBUG:
                    print("[DEBUG] Add new pattern %s"%pattern)
        
    return True

def generatePattern(method,url,params):
    pattern=[]
    pattern.append(method)
    pattern.append(url)
    paramKeys=[]
    for item in params.split("&"):
        paramKeys.append(item.split("=")[0])
    paramKeys.sort()
    pattern.extend(paramKeys)
    return pattern


def outputBlock(block):
    print("\n"+block+"\n\n\n\n")

def showHelp():
    print("\n+-----------------------------+")
    print("|  burplogfilter.py v0.1.0    |")
    print("|  Tony Lee                   |")
    print("|  tony1016@gmail.com         |")
    print("+-----------------------------+\n")
    print("Usage: python3 burplogfilter.py [options]\n")
    print("Options:")
    print("  -h                                  Show this showHelp")
    print("  -f filepath                         The BurpSuite log to analyze")
    print("  --host keyword, --host=keyword      Host name filter")
    print("  -v                                  Show debug message")
    print("\nExamples:")
    print("  python3 burplogfilter.py -f /tmp/burp.log --host=google.com")
    print("\n[!] to see help message of options run with '-h'")

if __name__ == '__main__':
    main()
