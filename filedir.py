# -*- coding:utf-8 -*-
# python文件和目录操作实例

import os
import shutil


# 1. 获取当前工作目录
currentpath = os.getcwd()
print "currentpath: ", currentpath

# 2. 获取指定目录下的所有文件和目录名
# print "os.listdir(): ", os.listdir("D:/ImageDownload/2017-4-10/")
for x in os.listdir("D:/ImageDownload/2017-4-10/"):
    print x

# 3. 判断目录或文件是否存在，判断是否为目录或文件， 删除文件
path = "D:/ImageDownload/2017-4-10/0.jpg"
if os.path.exists(path) and os.path.isfile(path):
    os.remove(path)
else:
    print path, 'not exist.'

# 4. 删除非空目录 os.removedirs只能删除空目录
path = "D:/ImageDownload/2017-4-10-1/"
if os.path.exists(path) and os.path.isdir(path):
    shutil.rmtree(path)
else:
    print path, 'not exist or not a dir.'

# 5. 判断是否是一个链接
print os.path.islink('http://www.baidu.com')

# 6. 分离路径的目录名和文件名, 分离结果为：('dirname', 'filename')
path = "D:/ImageDownload/2017-4-10/1.jpg"
print os.path.split(path)

# 7. 分离扩展名，分离结果为：('dirname/file', 'extname')
path = "D:/ImageDownload/2017-4-10/1.jpg"
print os.path.splitext(path)

# 8. 获取文件目录名
path = "D:/ImageDownload/2017-4-10/1.jpg"
print os.path.dirname(path)

# 9. 获取文件名
path = "D:/ImageDownload/2017-4-10/1.jpg"
print os.path.basename(path)
