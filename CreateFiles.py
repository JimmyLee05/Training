#coding=utf-8
'''
Created on 2012-5-29

@author: xiaochou
'''

import os
import time

def nsfile(s):
    '''The number of new expected documents'''
    #判断文件夹是否存在，如果不存在则创建
    b = os.path.exists("/Users/NanJunLi/Desktop/File")
    if b:
        print "File Exist!"
    else:
        os.mkdir("/Users/NanJunLi/Desktop/File")
    #生成文件
    for i in range(1,s+1):
        localTime = time.strftime("%Y%m%d%H%M%S",time.localtime())
        #print localtime
        filename = "/Users/NanJunLi/Desktop/File/"+localTime+""
        #a:以追加模式打开（必要时可以创建）append;b:表示二进制
        f = open(filename,'ab')
        testnote = '测试文件'
        f.write(testnote)
        f.close()
        #输出第几个文件和对应的文件名称
        print "file"+" "+str(i)+":"+str(localTime)+".txt"
        time.sleep(1)
    print "ALL Down"
    time.sleep(1)

if __name__ == '__main__':
    s = input("请输入需要生成的文件数：")
    nsfile(s)