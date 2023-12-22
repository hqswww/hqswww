import cv2
import numpy
from PIL import ImageGrab
import sys,time,ctypes
from random import random
import os
#os.chdir(sys.path[0])#使用的相对路径：cv2.imread('1.jpg')，但是python命令行所在的目录，不是当前.py程序的目录,加上此语句解决

#img_templ=cv2.imread(os.path.dirname(__file__+'play_button.png'))#模板图片

def app_path():
    if hasattr(sys,'frozen'):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)

#生成资源文件目录访问路径
def resource_path(relative_path):
    if hasattr(sys, 'frozen'):    #是否Bundle Resource
        base_path = sys._MEIPASS    #返回临时路径
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
img_path=resource_path(os.path.join('play_button.png'))
img_templ=cv2.imread(img_path)

THRESGHOLD=0.97 #参考相似度

class AUTO:
    def __init__(self,size,ratio,box):
        self.size=size
        self.ratio=ratio
        self.box=box
    #选取屏幕尺寸分辨率参数
    def confirm(self):
        #global box
        if self.size=='1':
            if self.ratio=='1':
                self.box=(49,27,68,53)#1920*1080
            elif self.ratio=='2':
                self.box=(63,35,82,59)#1920*1200
        elif self.size=='2':
            if self.ratio=='1':
                self.box=(84,48,108,80)#2560*1440
            elif self.ratio=='2':
                self.box=(85,49,107,79)#2560*1600
        #print(self.box)

    def mainLoo(self):
        #从游戏截图
        img_src=ImageGrab.grab(bbox=(self.box))#x1,y1,x2,y2
        #img_src.save('capture.jpg') #检查图片是否正确
        img_src=cv2.cvtColor(numpy.asarray(img_src),cv2.COLOR_RGB2BGR)

        #与模板匹配相似度
        result=cv2.matchTemplate(img_src,img_templ,cv2.TM_CCOEFF_NORMED)
        min_max=cv2.minMaxLoc(result)
        #输出匹配结果
        print('相似值为:',min_max)

        #匹配结果为三角形，对话模式
        if min_max[1]>THRESGHOLD:
            print('对话状态,鼠标单击状态')
            ctypes.windll.user32.mouse_event(2)#鼠标点击
            time.sleep(0.05+0.1*random())#休眠，间断时间
            ctypes.windll.user32.mouse_event(4)#鼠标松开
        else:
            print('当前非对话状态')

if __name__=='__main__':
    #判断是否有管理员权限
    if ctypes.windll.shell32.IsUserAnAdmin():
        print('已获取管理员权限')
        os.system("pause")
        #从用户获取数据
        print('当前屏幕的那种类型？？')
        size=input('1k请输入1,2k请输入2\n')
        print('请输入屏幕比例')
        ratio=input('16:9请输入1 , 16:10请输入2\n')
        #调用函数
        run=AUTO(size,ratio,'x')
        run.confirm()
        print('程序已经开始运行,结束程序直接关闭命令行就行')
        while True:
            time.sleep(0.3+0.2*random())
            run.mainLoo()
            #os.system("pause")
    else:
        print('请给予管理员权限')
        os.system("pause")
        ctypes.windll.shell32.ShellExecuteW(None,"runas", sys.executable, __file__, None, 1)
        #拉起UAC请求权限


'''
参考文章：
https://blog.csdn.net/weixin_46185214/article/details/106681135
https://blog.csdn.net/weixin_44214830/article/details/118338380
https://blog.csdn.net/baidu_38392815/article/details/115012223#:~:text=python%20%E6%89%93%E5%8C%85exe%20%28%E5%8C%85%E5%90%AB%E6%8A%8A%E8%B5%84%E6%BA%90%E6%96%87%E4%BB%B6%E6%89%93%E8%BF%9B%E5%8C%85%29%201%20pip%20install%20pyinstaller%20%E3%80%82,pyinstaller%20-F%20C%3A%5Cpyproj%5Cpys.py%20%EF%BC%8C%E7%94%9F%E6%88%90pys.spec%EF%BC%8Cbuild%E5%92%8Cdist%E6%96%87%E4%BB%B6%E5%A4%B9%20%28%E8%BF%99%E4%B8%A4%E4%B8%AA%E6%96%87%E4%BB%B6%E5%A4%B9%E5%8F%AF%E5%88%A0%EF%BC%8Cdist%E4%B8%AD%E5%85%B6%E5%AE%9E%E5%B7%B2%E7%BB%8F%E7%94%9F%E6%88%90%E4%BA%86exe%EF%BC%8C%E4%BD%86%E6%98%AF%E8%BF%90%E8%A1%8C%E4%BC%9A%E6%8A%A5%E9%94%99%EF%BC%8C%E5%9B%A0%E4%B8%BA%E8%B5%84%E6%BA%90%E6%89%BE%E4%B8%8D%E5%88%B0%EF%BC%8C%E5%A6%82%E6%9E%9C%E6%B2%A1%E6%9C%89%E7%94%A8%E5%88%B0%E8%B5%84%E6%BA%90%E7%9A%84%E8%AF%9D%E6%98%AF%E5%8F%AF%E4%BB%A5%E8%BF%90%E8%A1%8C%E7%9A%84%29%E3%80%82%204%20%E6%89%93%E5%BC%80pys.spec%E3%80%82%20%E7%94%A8%E8%AE%B0%E4%BA%8B%E6%9C%AC%E7%AD%89%E6%89%93%E5%BC%80pys.spec%EF%BC%8C%E5%86%85%E5%AE%B9%E5%A4%A7%E6%A6%82%E8%BF%99%E6%A0%B7%EF%BC%9A
'''