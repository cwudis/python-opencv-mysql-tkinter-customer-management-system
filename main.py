from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font
import pymysql
from tkinter import messagebox
import tkinter.simpledialog
import cv2, os, math, operator
from PIL import Image
from functools import reduce
from tkinter.messagebox import *

Permissions = False  # 超级管理权限
total = 0
z = 0
recogname = None


# 主界面
class MainInterface:

    def __init__(self, subInterface):
        subInterface.destroy()  # 销毁子界面
        self.window = tk.Tk()
        self.window.title("主窗口")
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

        # 文本显示 _Label
        self.Label0 = tk.Label(self.window, text="顾客营销管理系统", font=("黑体", 40))
        self.Label0.pack(pady=70, padx=30)

        # 按钮显示_Button
        self.Button0 = tk.Button(self.window, text="管理员登录", font=tkinter.font.Font(size=16),
                                 command=lambda: ADLoginInterface(self.window),
                                 width=20, height=2, fg='white', bg='gray')
        self.Button0.pack(pady=10, padx=30)
        self.Button1 = tk.Button(self.window, text="顾客登录", font=tkinter.font.Font(size=16),
                                 command=lambda: CLoginInterface(self.window),
                                 width=20, height=2, fg='white', bg='gray')
        self.Button1.pack(pady=10, padx=30)
        self.Button2 = tk.Button(self.window, text="退出", font=tkinter.font.Font(size=16), command=self.window.destroy,
                                 width=20, height=2, fg='white', bg='gray')
        self.Button2.pack(pady=10, padx=30)

        self.window.mainloop()  # 主窗口循环


# 管理员登录界面
class ADLoginInterface:

    def __init__(self, subInterface):
        subInterface.destroy()  # 销毁子界面
        self.window = tk.Tk()
        self.window.title("管理员登录界面")
        screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
        screenheight = self.window.winfo_screenheight()  # 获取屏幕高
        # 使窗口位于屏幕中央
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

        label0 = tk.Label(self.window, text="登录", bg='SkyBlue', font=('宋体', 20), width=70, height=2)
        label0.pack()

        label1 = tk.Label(self.window, text="账号", font=('宋体', 14))
        label1.pack(pady=25)
        self.account = tk.Entry(self.window, width=30, font=tkinter.font.Font(size=14), bg='Ivory')
        self.account.pack()

        label1 = tk.Label(self.window, text="密码", font=('宋体', 14))
        label1.pack(pady=25)
        self.password = tk.Entry(self.window, width=30, font=tkinter.font.Font(size=14), bg='Ivory', show='*')
        self.password.pack()

        button1 = tk.Button(self.window, text="登录", width=8, font=tkinter.font.Font(size=12), command=self.login)
        button1.pack(pady=40)
        button1 = tk.Button(self.window, text="返回", width=8, font=tkinter.font.Font(size=12), command=self.back)
        button1.pack()

        self.window.mainloop()

    def login(self):
        _account = None
        _password = None
        _remark = None
        # 数据库连接，查询管理员信息表
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123', db='csm', charset='utf8')
        curses = conn.cursor()
        sql = "select 账号, 密码, 备注 from lad where 账号 = '%s'" % (self.account.get())
        try:
            curses.execute(sql)
            results = curses.fetchall()
            for row in results:
                _account = row[0]
                _password = row[1]
                _remark = row[2]
        except ValueError:
            print("Error: unable to fetch data")
            messagebox.showinfo("账号或密码不正确！")
        conn.close()

        if self.account.get() == _account and self.password.get() == _password:
            # 如果登录的是超级管理员账号，赋予超级管理员权限
            if _remark == '超级管理员':
                global Permissions  # global：声明或定义全局变量，以便使用全局变量
                Permissions = True
            ActionSelectionInterface(self.window)  # 进入选择操作界面
        else:
            messagebox.showinfo('警告！', '账号或密码不正确！')

    def back(self):
        MainInterface(self.window)  # 返回主界面


# 顾客登录界面
class CLoginInterface:
    def __init__(self, subInterface):
        subInterface.destroy()  # 销毁子界面
        self.window = tk.Tk()
        self.window.title("顾客登录界面")
        screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
        screenheight = self.window.winfo_screenheight()  # 获取屏幕高
        # 使窗口位于屏幕中央
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

        self._CId = StringVar()
        self._password = StringVar()

        label0 = tk.Label(self.window, text="登录", bg='SkyBlue', font=('宋体', 20), width=70, height=2)
        label0.pack()

        label1 = tk.Label(self.window, text="编号", font=('宋体', 14))
        label1.pack(pady=25)
        self.account2 = tk.Entry(self.window, width=30, font=tkinter.font.Font(size=14), bg='Ivory')
        self.account2.pack()

        label1 = tk.Label(self.window, text="密码", font=('宋体', 14))
        label1.pack(pady=25)
        self.password = tk.Entry(self.window, width=30, font=tkinter.font.Font(size=14), bg='Ivory', show='*')
        self.password.pack()

        button1 = tk.Button(self.window, text="账号登录", width=15, font=tkinter.font.Font(size=12), command=self.login)
        button1.pack(pady=30)
        button2 = tk.Button(self.window, text="人脸登录", width=15, font=tkinter.font.Font(size=12),
                            command=self.facelogin)
        button2.pack()

        button3 = tk.Button(self.window, text="返回", width=15, font=tkinter.font.Font(size=12), command=self.back)
        button3.pack(pady=30)

        self.window.mainloop()

    # 账号登录
    def login(self):
        _CId = None
        _password = None
        # 数据库连接，查询顾客信息表
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123', db='csm', charset='utf8')
        curses = conn.cursor()
        sql = "select 顾客编号, 姓名, 性别, 联系方式, 级别, 优惠劵, 注册时间, 密码 from lcustomer where 顾客编号 = '%s'" % (
            self.account2.get())
        global z
        z = self.account2.get()
        try:
            curses.execute(sql)
            results = curses.fetchall()
            for row in results:
                _CId = row[0]
                _password = row[7]
        except ValueError:
            print("Error: unable to fetch data")
            messagebox.showinfo("账号或密码不正确！")
        conn.close()
        if self.account2.get() == _CId and self.password.get() == _password:
            MallOperation(self.window)  # 进入购物中心操作界面
        else:
            messagebox.showinfo('警告！', '账号或密码不正确！')

    # 人脸登录
    def facelogin(self):
        _CId = None
        _password = None
        # 数据库连接，查询顾客信息表
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123', db='csm', charset='utf8')
        curses = conn.cursor()
        sql = "select 顾客编号, 姓名, 性别, 联系方式, 级别, 优惠劵, 注册时间, 密码 from lcustomer where 顾客编号 = '%s'" % (
            self.account2.get())
        try:
            curses.execute(sql)
            results = curses.fetchall()
            for row in results:
                _CId = row[0]
                _password = row[7]
            _CId = self.account2.get()
            global z
            z = self.account2.get()
            if _CId == "":
                showinfo(title="错误", message='请输入顾客编号！')
            else:
                a = cxk(_CId)
            if (a <= 100):  # 若差度在100内，可通过验证
                tkinter.messagebox.showinfo("登录成功！")
                MallOperation(self.window)
            elif (a == 200.0):
                showinfo(title='错误', message='数据库无该顾客人脸信息，请先进行人脸注册！')
            else:
                print("没有通过验证！ diff=%4.2f" % a)
        except ValueError:
            showinfo(title='错误', message='输入错误，请重新输入！')
        conn.close()

    def back(self):
        MainInterface(self.window)  # 返回主界面


# 人脸信息录入
def makeFace(facename, msg):
    print(msg)  # 显示提示信息
    cap = cv2.VideoCapture("videos/002.mp4")  # 打开摄像头
    cv2.namedWindow('face_recognition', cv2.WINDOW_NORMAL)  # 窗口大小可设置
    cv2.resizeWindow('face_recognition', 768, 432)  # 大小
    cv2.moveWindow('face_recognition', 300, 100)  # 位置
    while (cap.isOpened()):  # 如果摄像头处于打开状态，则...
        try:
            ret, img = cap.read()  # 读取图像
            if ret == True:  # 读取成功
                cv2.imshow("face_recognition", img)  # 显示图像
                k = cv2.waitKey(100)  # 每0.1秒读一次键盘
                if k == ord("z") or k == ord("Z"):  # 如果输入z
                    cv2.imwrite(facename, img)  # 把读取的img保存至facename文件
                    image = cv2.imread(facename)  # 读取刚刚保存的facename文件至image变量，作为下面人脸识别函数的参数
                    faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                                         flags=cv2.CASCADE_SCALE_IMAGE)
                    # print(faces)
                    (x, y, w, h) = (faces[0][0], faces[0][1], faces[0][2], faces[0][3])  # 取出第一张人脸区域
                    #                     print(x,y,w,h)
                    image1 = Image.open(facename).crop((x, y, x + w, y + h))  # 抓取人脸区域的图像并存至image1变量
                    image1 = image1.resize((200, 200), Image.ANTIALIAS)  # 把取得的人脸区域的分辨率变为200x200
                    image1.save(facename)  # 把经过处理的人脸文件保存至facename文件
                    break
        except Exception as e:
            print(e)
            continue
    cap.release()  # 关闭摄像头
    cv2.destroyAllWindows()  # 关闭窗口
    return


# 人脸登录检测
def cxk(number):
    diff = 0.0
    global recogname
    recogname = "%s_recogface.jpg" % number  # 预存的人脸文件
    loginname = "%s_loginface.jpg" % number  # 登录者的人脸文件
    os.system("cls")  # 清屏
    if (os.path.exists(recogname)):  # 如果预存的人脸文件已存在
        msg = "摄像头打开后按 z 键进行拍照对比！"
        makeFace(loginname, msg)  # 创建登录者人脸文件
        pic1 = Image.open(recogname)  # 打开预存的人脸文件
        pic2 = Image.open(loginname)  # 打开登录者人脸文件
        h1 = pic1.histogram()  # 取预存片文件的直方图信息
        h2 = pic2.histogram()  # 取登录者图片的直方图信息
        diff = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))  # 计算两个图形差异度
    else:  # 如果预存的人脸文件不存在
        diff = 200.0
    return diff


# 选择操作界面
class ActionSelectionInterface:
    def __init__(self, subInterface):
        subInterface.destroy()  # 销毁子界面
        self.window = tk.Tk()
        self.window.title("选择操作界面")
        screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
        screenheight = self.window.winfo_screenheight()  # 获取屏幕高
        # 使窗口位于屏幕中央
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

        label0 = tk.Label(self.window, text="选择要进行的操作", bg='SkyBlue', font=('宋体', 20), width=70, height=2)
        label0.pack(pady=100)

        # 按钮
        button1 = ttk.Button(self.window, text="操作商品信息", width=30,
                             command=lambda: GoodsInformationOperation(self.window))
        button1.pack(pady=10)
        button2 = ttk.Button(self.window, text='操作顾客信息', width=30,
                             command=lambda: CustomerInformationOperation(self.window))
        button2.pack(pady=10)

        if Permissions is True:
            button3 = ttk.Button(self.window, text='操作管理员信息', width=30,
                                 command=lambda: ADInformationOperation(self.window))
            button3.pack(pady=10)
        button4 = ttk.Button(self.window, text='返回', width=30, command=self.back)
        button4.pack(pady=10)

        self.window.mainloop()  # 主消息循环

    def back(self):
        global Permissions
        Permissions = False
        ADLoginInterface(self.window)


# 购物中心操作界面
class MallOperation:
    def __init__(self, subInterface):
        subInterface.destroy()  # 销毁子界面
        self.window = tk.Tk()
        self.window.title("购物中心操作界面")
        screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
        screenheight = self.window.winfo_screenheight()  # 获取屏幕高
        # 使窗口位于屏幕中央
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 700, (screenwidth - 800) / 2, (screenheight - 700) / 2))

        self.start

        label = tk.Label(self.window, text="购物中心", bg='SkyBlue', font=('宋体', 20), width=70, height=1)
        label.pack()

        # 商品内容列表
        self.frameTopList = tk.Frame(width=650, height=400)
        self.frameTopList.pack(pady=1)

        self.columns = ('商品编号', '商品名称', '商品类别', '商品价格 (单位元)')
        self.tree = ttk.Treeview(self.frameTopList, show='headings', height=6, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frameTopList, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        # 表格的标题
        self.tree.column('商品编号', width=75, anchor='center')  # 表示列，不显示
        self.tree.column('商品名称', width=150, anchor='center')
        self.tree.column("商品类别", width=100, anchor='center')
        self.tree.column("商品价格 (单位元)", width=150, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.id = []
        self.name = []
        self.type = []
        self.price = []
        self.stock = []
        # 数据库操作 查询商品信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select 商品编号, 商品名称, 商品类别, 商品价格, 商品库存 from lgoods "  # 查询商品信息表
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.name.append(row[1])
                self.type.append(row[2])
                self.price.append(row[3])
                self.stock.append(row[4])
        except ValueError:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()  # 关闭连接
        # 写入数据
        for i in range(len(self.id)):
            if int(self.stock[i]) > 0:
                self.tree.insert('', i, values=(
                    self.id[i], self.name[i], self.type[i], self.price[i]))

        for col in self.columns:
            self.tree.heading(col, text=col)

        self.frameCenter = tk.Frame(width=200, height=230)
        self.frameCenter.pack(pady=10)

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置
        self.CenterButton1 = ttk.Button(self.frameCenter, text='添加到购物车', width=20, command=self.selection)
        self.CenterButton2 = ttk.Button(self.frameCenter, text='查询优惠劵', width=20, command=self.test)
        self.CenterButton3 = ttk.Button(self.frameCenter, text='结算', width=20, command=self.account)
        self.CenterButton4 = ttk.Button(self.frameCenter, text='退出', width=20, command=self.back)
        self.text1 = tk.Text(self.frameCenter, width=20, height=1)
        self.CenterButton1.pack()
        self.CenterButton2.pack()
        self.text1.pack()
        self.CenterButton3.pack()
        self.CenterButton4.pack()

        # 位置
        self.frameBottom = tk.Frame(width=650, height=100)
        self.frameBottom.pack(pady=5)

        # 购物车界面
        self.label = tk.Label(self.frameBottom, text='购物车', bg='SkyBlue', font=('宋体', 20), width=40, height=1)
        self.label.pack()
        self.text2 = tk.Text(self.frameBottom, height=10)
        self.text2.pack()

        # 结算界面
        self.label = tk.Label(self.window, text="结算中心", bg='SkyBlue', font=('宋体', 20), width=40, height=1)
        self.text3 = tk.Text(self.window, height=3)
        self.label.pack(pady=10)
        self.text3.pack()

        self.window.mainloop()

    def start(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()

    def selection(self):
        file = open('a.txt', 'r')
        inspection = file.read()
        num = 1
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请选中一条商品')
        else:
            # if int(inspection) != i:
            ii = int(inspection)
            if int(self.stock[ii - 1]) > 0:
                self.text2.insert("end", "商品名称:" + str(self.name[ii - 1]) + "       " + "商品价格:" + str(
                    self.price[ii - 1]) + "      " + "数量:" + str(num) + "\n")
            else:
                messagebox.showinfo('提示！', '该商品无库存')

        global total
        total += int(self.price[ii - 1])

        self.id = StringVar()
        file = open('a.txt', 'r')
        self.id = file.read()
        file.close()

        if int(self.stock[ii - 1]) > 0:
            # 数据库操作 查询商品信息表
            conn = pymysql.connect(
                host="localhost", port=3306,
                user="root", passwd="123",
                database='csm', charset='utf8'
            )  # 创建连接
            cursor = conn.cursor()  # 获取游标对象
            sql = "update lgoods set 商品库存 = '%s' where 商品编号 = '%s'" % (
                (int(self.stock[ii - 1]) - 1), self.id)  # 修改商品信息表中对应商品编号的商品库存
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                conn.commit()
            except ValueError:
                conn.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '数据库连接失败！')
            conn.close()  # 关闭连接

        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行
        self.rowInfo = self.tree.item(self.row, 'values')
        a = self.rowInfo[0]
        file = open('a.txt', 'w+')
        file.seek(0)
        file.truncate()
        file.write(a)
        file.close()

    # 查看优惠卷
    def test(self):
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select 顾客编号, 优惠劵 from lcustomer where 顾客编号 = '%s'" % (z)
        try:
            # 执行sql语句
            cursor.execute(sql)
            results = cursor.fetchmany(2)
            for row in results:
                cid = row[0]
                coupon = row[1]
        except ValueError:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        self.text1.insert("end", "优惠卷:" + str(coupon) + "折" + "\n")
        conn.close()  # 关闭连接

    # 结算
    def account(self):
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select 级别, 优惠劵 from lcustomer where 顾客编号 = '%s'" % (z)
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchmany(2)
        for row in results:
            level = row[0]
            coupon = row[1]
        if level == 'vip':
            price = int(total * int(coupon) * 0.1)
            self.text3.insert("end", "vip使用优惠劵打" + str(coupon) + "折," + "应付:" + str(price) + "元" + "\n")
        else:
            self.text3.insert("end", "普通顾客无优惠劵, 应付:" + str(total) + "元" + "\n")
        conn.close()  # 关闭连接

    def back(self):
        MainInterface(self.window)  # 返回主界面


# 商品信息操作界面
class GoodsInformationOperation:
    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title("商品信息操作界面")
        screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
        screenheight = self.window.winfo_screenheight()  # 获取屏幕高
        # 使窗口位于屏幕中央
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 700, (screenwidth - 800) / 2, (screenheight - 700) / 2))
        self.start

        self.frameLeftTop = tk.Frame(width=300, height=200)
        self.frameRightTop = tk.Frame(width=200, height=230)
        self.frameCenter = tk.Frame(width=650, height=400)
        self.frameBottom = tk.Frame(width=650, height=50)

        self.topTitle = Label(self.frameLeftTop)
        self.topTitle.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.leftTopFrame = tk.Frame(self.frameLeftTop)
        self.GID = StringVar()  # 声明商品编号
        self.GName = StringVar()  # 声明商品名称
        self.GType = StringVar()  # 声明商品类别
        self.GPrice = StringVar()  # 声明商品价格
        self.GStock = StringVar()  # 声明商品库存

        self.rightTopGoodsNameLabel = Label(self.frameLeftTop, text='请输入商品名', font=('宋体', 15))
        self.rightTopGoodsNameEntry = Entry(self.frameLeftTop, textvariable=self.GName, font=('Verdana', 15))
        self.rightTopGoodsNameButton = Button(self.frameLeftTop, text='搜索', width=20, command=self.find)
        self.rightTopGoodsNameLabel.grid(row=1, column=1)  # 位置信息
        self.rightTopGoodsNameEntry.grid(row=2, column=1)
        self.rightTopGoodsNameButton.grid(row=3, column=1)

        # 定义下方中心列表区域
        self.columns = ('商品编号', '商品名称', '商品类别', '商品价格 (单位元)', '商品库存')
        self.tree = ttk.Treeview(self.frameCenter, show='headings', height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frameCenter, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        # 表格的标题
        self.tree.column('商品编号', width=75, anchor='center')  # 表示列，不显示
        self.tree.column('商品名称', width=100, anchor='center')
        self.tree.column("商品类别", width=100, anchor='center')
        self.tree.column("商品价格 (单位元)", width=150, anchor='center')
        self.tree.column("商品库存", width=75, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)
        self.window.protocol('WM_DELETE_WINDOW', self.back)  # 捕捉右上角关闭点击

        self.id = []
        self.name = []
        self.type = []
        self.price = []
        self.stock = []
        # 数据库操作 查询商品信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select * from lgoods"  # 查询商品信息表
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.name.append(row[1])
                self.type.append(row[2])
                self.price.append(row[3])
                self.stock.append(row[4])

        except ValueError:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()  # 关闭连接
        # 写入数据
        for i in range(len(self.id)):
            self.tree.insert('', i, values=(
                self.id[i], self.name[i], self.type[i], self.price[i], self.stock[i]))
        for col in self.columns:
            self.tree.heading(col, text=col)

        # 定义右上方区域
        self.rightTopTitle = Label(self.frameRightTop, text='选择操作', font=("宋体", 18))

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置
        self.rightTopButton1 = ttk.Button(self.frameRightTop, text='添加商品', width=20,
                                          command=lambda: AddGoods(self.window))
        self.rightTopButton2 = ttk.Button(self.frameRightTop, text='修改选中商品', width=20,
                                          command=lambda: EditGoodsInformation(self.window))
        self.rightTopButton3 = ttk.Button(self.frameRightTop, text='删除选中商品', width=20, command=self.delRow)

        # 位置设置
        self.rightTopTitle.grid(row=1, column=0, pady=10)
        self.rightTopButton1.grid(row=2, column=0, padx=20, pady=10)
        self.rightTopButton2.grid(row=3, column=0, padx=20, pady=10)
        self.rightTopButton3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frameLeftTop.grid(row=0, column=0, padx=2, pady=5)
        self.frameRightTop.grid(row=0, column=1, padx=30, pady=30)
        self.frameCenter.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frameBottom.grid(row=2, column=0, columnspan=2)

        self.frameLeftTop.grid_propagate(True)
        self.frameRightTop.grid_propagate(True)
        self.frameCenter.grid_propagate(True)
        self.frameBottom.grid_propagate(True)

        self.frameLeftTop.tkraise()  # 开始显示主菜单
        self.frameRightTop.tkraise()  # 开始显示主菜单
        self.frameCenter.tkraise()  # 开始显示主菜单
        self.frameBottom.tkraise()  # 开始显示主菜单

        self.window.mainloop()

    def start(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()

    def find(self):
        FindGoodsInformation(self.window, self.rightTopGoodsNameEntry.get())

    def back(self):
        ActionSelectionInterface(self.window)  # 返回操作选择界面

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行
        self.rowInfo = self.tree.item(self.row, 'values')
        a = self.rowInfo[0]
        file = open('a.txt', 'w+')
        file.seek(0)
        file.truncate()
        file.write(a)
        file.close()

    def delRow(self):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请选中一条商品信息信息')
        else:
            # 数据库操作 查询商品信息表
            conn = pymysql.connect(
                host="localhost", port=3306,
                user="root", passwd="123",
                database='csm', charset='utf8'
            )  # 创建连接
            cursor = conn.cursor()  # 获取游标对象
            sql_0 = "delete from lgoods where 商品编号 = '%s'"
            sql = sql_0 % (self.rowInfo[0])  # 删除语句
            try:
                prompt = messagebox.askyesnocancel('警告！', '是否删除所选信息？')
                if prompt:
                    if int(self.rowInfo[4]) != 0:
                        messagebox.showinfo('警告！', '商品库存未清空，无法删除！')
                    else:
                        # 执行sql语句
                        cursor.execute(sql)
                        # 提交到数据库执行
                        conn.commit()
                        a = self.id.index(self.rowInfo[0])
                        del self.id[a]
                        del self.name[a]
                        del self.type[a]
                        del self.price[a]
                        del self.stock[a]

                        self.tree.delete(self.tree.selection()[0])  # 删除所选行
                        messagebox.showinfo('提示！', '删除成功！')
            except ValueError:
                # conn.rollback  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败！')
            conn.close()  # 关闭连接
            file = open('a.txt', 'r+')
            file.seek(0)
            file.truncate()
            file.close()
            file = open('a.txt', 'w+')
            file.write('未选中')
            file.close()


# 顾客信息操作界面
class CustomerInformationOperation:
    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title("顾客信息操作界面")
        screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
        screenheight = self.window.winfo_screenheight()  # 获取屏幕高
        # 使窗口位于屏幕中央
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 700, (screenwidth - 800) / 2, (screenheight - 700) / 2))

        self.frameLeftTop = tk.Frame(width=300, height=200)
        self.frameRightTop = tk.Frame(width=200, height=200)
        self.frameCenter = tk.Frame(width=500, height=400)
        self.frameBottom = tk.Frame(width=650, height=50)

        self.topTitle = Label(self.frameLeftTop)
        self.topTitle.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.leftTopFrame = tk.Frame(self.frameLeftTop)
        self.CId = StringVar()  # 声明顾客编号
        self.CName = StringVar()  # 声明姓名
        self.CSex = StringVar()  # 声明性别
        self.CNum = StringVar()  # 声明联系方式
        self.CLevel = StringVar()  # 声明级别
        self.CCoupon = StringVar()  # 声明优惠劵
        self.CData = StringVar()  # 声明注册时间
        self.CPassword = StringVar()  # 声明密码

        self.rightTopNameLabel = Label(self.frameLeftTop, text='请输入姓名', font=('宋体', 15))
        self.rightTopNameEntry = Entry(self.frameLeftTop, textvariable=self.CName, font=('Verdana', 15))
        self.rightTopNameButton = Button(self.frameLeftTop, text='搜索', width=20, command=self.find)
        self.rightTopNameLabel.grid(row=1, column=1)  # 位置信息
        self.rightTopNameEntry.grid(row=2, column=1)
        self.rightTopNameButton.grid(row=3, column=1)

        # 定义下方中心列表区域
        self.columns = ('顾客编号', '姓名', '性别', '联系方式', '级别', '优惠劵', '注册时间', '密码')
        self.tree = ttk.Treeview(self.frameCenter, show='headings', height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frameCenter, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        # 表格的标题
        self.tree.column('顾客编号', width=75, anchor='center')  # 表示列，不显示
        self.tree.column('姓名', width=50, anchor='center')
        self.tree.column("性别", width=50, anchor='center')
        self.tree.column("联系方式", width=100, anchor='center')
        self.tree.column("级别", width=50, anchor='center')
        self.tree.column("优惠劵", width=75, anchor='center')
        self.tree.column("注册时间", width=100, anchor='center')
        self.tree.column("密码", width=75, anchor='center')
        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)
        self.window.protocol('WM_DELETE_WINDOW', self.back)  # 捕捉右上角关闭点击

        self.id = []
        self.name = []
        self.sex = []
        self.num = []
        self.level = []
        self.coupon = []
        self.data = []
        self.password = []
        # 数据库操作 查询顾客信息表
        conn = pymysql.connect(
            host="localhost", port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select * from lcustomer"  # 查询顾客信息表
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.name.append(row[1])
                self.sex.append(row[2])
                self.num.append(row[3])
                self.level.append(row[4])
                self.coupon.append(row[5])
                self.data.append(row[6])
                self.password.append(row[7])
        except ValueError:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()  # 关闭连接
        # 写入数据
        for i in range(len(self.id)):
            self.tree.insert('', i, values=(
                self.id[i], self.name[i], self.sex[i], self.num[i], self.level[i], self.coupon[i],
                self.data[i], self.password[i]))
        for col in self.columns:
            self.tree.heading(col, text=col)

        # 定义右上方区域
        self.rightTopTitle = Label(self.frameRightTop, text='选择操作', font=("宋体", 18))

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置
        self.rightTopButton1 = ttk.Button(self.frameRightTop, text='添加顾客', width=20,
                                          command=lambda: AddReader(self.window))
        self.rightTopButton2 = ttk.Button(self.frameRightTop, text='修改选中顾客', width=20,
                                          command=lambda: EditCustomerInformation(self.window))
        self.rightTopButton3 = ttk.Button(self.frameRightTop, text='删除选中顾客', width=20, command=self.delRow)
        self.rightTopButton4 = ttk.Button(self.frameRightTop, text='顾客人脸录入', width=20, command=self.facesignin)

        # 位置设置
        self.rightTopTitle.grid(row=1, column=0, pady=10)
        self.rightTopButton1.grid(row=2, column=0, padx=20, pady=10)
        self.rightTopButton2.grid(row=3, column=0, padx=20, pady=10)
        self.rightTopButton3.grid(row=4, column=0, padx=20, pady=10)
        self.rightTopButton4.grid(row=5, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frameLeftTop.grid(row=0, column=0, padx=2, pady=5)
        self.frameRightTop.grid(row=0, column=1, padx=30, pady=30)
        self.frameCenter.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frameBottom.grid(row=2, column=0, columnspan=2)

        self.frameLeftTop.grid_propagate(True)
        self.frameRightTop.grid_propagate(True)
        self.frameCenter.grid_propagate(True)
        self.frameBottom.grid_propagate(True)

        self.frameLeftTop.tkraise()  # 开始显示主菜单
        self.frameRightTop.tkraise()  # 开始显示主菜单
        self.frameCenter.tkraise()  # 开始显示主菜单
        self.frameBottom.tkraise()  # 开始显示主菜单

        self.window.mainloop()

    def find(self):
        FindCustomerInformation(self.window, self.rightTopNameEntry.get())

    def back(self):
        ActionSelectionInterface(self.window)  # 返回操作选择界面

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行
        self.rowInfo = self.tree.item(self.row, 'values')
        a = self.rowInfo[0]
        file = open('a.txt', 'w+')
        file.seek(0)
        file.truncate()
        file.write(a)
        file.close()

    def delRow(self):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请选中一条顾客信息')
        else:
            # 数据库操作 查询顾客信息表
            conn = pymysql.connect(
                host="localhost", port=3306,
                user="root", passwd="123",
                database='csm', charset='utf8'
            )  # 创建连接
            cursor = conn.cursor()  # 获取游标对象
            sql = "delete from lcustomer where 顾客编号 = '%s'" % (self.rowInfo[0])  # 删除语句

            try:
                prompt = messagebox.askyesnocancel('警告！', '是否删除所选信息？')
                if prompt:
                    con = self.rowInfo[4]
                    if con == "vip":
                        messagebox.showinfo('警告！', 'vip用户无法删除！')
                    else:
                        # 执行sql语句
                        cursor.execute(sql)
                        # 提交到数据库执行
                        conn.commit()
                        a = self.id.index(self.rowInfo[0])
                        del self.id[a]
                        del self.name[a]
                        del self.sex[a]
                        del self.num[a]
                        del self.level[a]
                        del self.coupon[a]
                        del self.data[a]
                        self.tree.delete(self.tree.selection()[0])  # 删除所选行
                        messagebox.showinfo('提示！', '删除成功！')
            except ValueError:
                # conn.rollback  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败！')
            conn.close()  # 关闭连接

        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()

        # 人脸注册

    def facesignin(self):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        recogname = "%s_recogface.jpg" % inspection
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请选中一条顾客信息')
        elif (os.path.exists(recogname)):
            showinfo(title="错误", message='该顾客已保存人脸信息，可直接登录！')
        else:
            msg = "摄像头打开后按 z 键进行拍照！\n"
            makeFace(recogname, msg)  # 建立预存人脸文件
            showinfo(title='确认', message='人脸信息保存成功！')
            conn = pymysql.connect(
                host="localhost", port=3306,
                user="root", passwd="123",
                database='csm', charset='utf8'
            )  # 创建连接
            cursor = conn.cursor()  # 获取游标对象
            sql = "update lcustomer set 级别 = 'vip', 优惠劵 = '%s' where 顾客编号 = '%s'" % (
                self.HowCoupon(), self.rowInfo[0])  # 修改顾客信息表中对应顾客编号的级别等信息
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                conn.commit()
                messagebox.showinfo('提示！', '更新成功！')
            except ValueError:
                conn.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '数据库连接失败！')
            conn.close()  # 关闭连接

    def HowCoupon(self):
        CCoupon = tkinter.simpledialog.askstring(title='信息', prompt='请输入：', initialvalue='几折')
        return CCoupon


# 管理员信息操作界面
class ADInformationOperation:
    def __init__(self, subInterface):
        self.rowInfo = None
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title("管理员信息操作界面")
        screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
        screenheight = self.window.winfo_screenheight()  # 获取屏幕高
        # 使窗口位于屏幕中央
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

        self.frameLeftTop = tk.Frame(width=300, height=200)
        self.frameRightTop = tk.Frame(width=200, height=200)
        self.frameCenter = tk.Frame(width=450, height=400)
        self.frameBottom = tk.Frame(width=650, height=50)

        self.topTitle = Label(self.frameLeftTop)
        self.topTitle.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.leftTopFrame = tk.Frame(self.frameLeftTop)
        self.varAccount = StringVar()  # 声明账号
        self.varPassword = StringVar()  # 声明密码
        self.varRemark = StringVar()  # 声明备注

        self.rightTopAccountLabel = Label(self.frameLeftTop, text='请输入账号', font=("宋体", 15))
        self.rightTopAccountEntry = Entry(self.frameLeftTop, textvariable=self.varAccount, font=('Verdana', 15))
        self.rightTopAccountButton = Button(self.frameLeftTop, text='搜索', width=20, command=self.find)
        self.rightTopAccountLabel.grid(row=1, column=1)  # 位置信息
        self.rightTopAccountEntry.grid(row=2, column=1)
        self.rightTopAccountButton.grid(row=3, column=1)

        # 定义下方中心列表区域
        self.columns = ('账号', '密码', '备注')
        self.tree = ttk.Treeview(self.frameCenter, show='headings', height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frameCenter, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        # 表格的标题
        self.tree.column('账号', width=150, anchor='center')  # 表示列，不显示
        self.tree.column('密码', width=150, anchor='center')
        self.tree.column("备注", width=150, anchor='center')
        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)
        self.window.protocol('WM_DELETE_WINDOW', self.back)  # 捕捉右上角关闭点击

        self.account = []
        self.password = []
        self.remark = []
        # 数据库操作 查询管理员信息表
        conn = pymysql.connect(
            host="localhost", port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select * from Lad"  # 查询管理员信息表
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.account.append(row[0])
                self.password.append(row[1])
                self.remark.append(row[2])
        except ValueError:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()  # 关闭连接
        # 写入数据
        for i in range(len(self.account)):
            self.tree.insert('', i, values=(self.account[i], self.password[i], self.remark[i]))
        for col in self.columns:
            self.tree.heading(col, text=col)

        # 定义右上方区域
        self.rightTopTitle = Label(self.frameRightTop, text='选择操作', font=("宋体", 18))

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置
        self.rightTopButton1 = ttk.Button(self.frameRightTop, text='添加管理员', width=20,
                                          command=lambda: AddAD(self.window))
        self.rightTopButton2 = ttk.Button(self.frameRightTop, text='修改选择管理员密码', width=20,
                                          command=lambda: EditADInformation(self.window))
        self.rightTopButton3 = ttk.Button(self.frameRightTop, text='删除选中管理员', width=20, command=self.delRow)

        # 位置设置
        self.rightTopTitle.grid(row=1, column=0, pady=10)
        self.rightTopButton1.grid(row=2, column=0, padx=20, pady=10)
        self.rightTopButton2.grid(row=3, column=0, padx=20, pady=10)
        self.rightTopButton3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frameLeftTop.grid(row=0, column=0, padx=2, pady=5)
        self.frameRightTop.grid(row=0, column=1, padx=30, pady=30)
        self.frameCenter.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frameBottom.grid(row=2, column=0, columnspan=2)

        self.frameLeftTop.grid_propagate(True)
        self.frameRightTop.grid_propagate(True)
        self.frameCenter.grid_propagate(True)
        self.frameBottom.grid_propagate(True)

        self.frameLeftTop.tkraise()  # 开始显示主菜单
        self.frameRightTop.tkraise()  # 开始显示主菜单
        self.frameCenter.tkraise()  # 开始显示主菜单
        self.frameBottom.tkraise()  # 开始显示主菜单

        self.window.mainloop()

    def start(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()

    def find(self):
        FindADInformation(self.window, self.rightTopAccountEntry.get())

    def back(self):
        ActionSelectionInterface(self.window)  # 返回操作选择界面

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行
        self.rowInfo = self.tree.item(self.row, 'values')
        a = self.rowInfo[0]
        file = open('a.txt', 'w+')
        file.seek(0)
        file.truncate()
        file.write(a)
        file.close()

    def delRow(self):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请选中一条管理员信息')
        else:
            # 数据库操作 查询管理员信息表
            conn = pymysql.connect(
                host="localhost", port=3306,
                user="root", passwd="123",
                database='csm', charset='utf8'
            )  # 创建连接
            cursor = conn.cursor()  # 获取游标对象
            sql = "delete from Lad where 账号 = '%s'" % (self.rowInfo[0])  # 删除语句
            try:
                prompt = messagebox.askyesnocancel('警告！', '是否删除所选信息？')
                if prompt is True:
                    if self.rowInfo[2] == '超级管理员':
                        messagebox.showinfo('警告！', '不能删除超级管理员账户！')
                    else:
                        # 执行sql语句
                        cursor.execute(sql)
                        # 提交到数据库执行
                        conn.commit()
                        a = any(self.rowInfo[0])
                        del self.account[a]
                        del self.password[a]
                        del self.remark[a]
                        self.tree.delete(self.tree.selection()[0])  # 删除所选行
                        messagebox.showinfo('提示！', '删除成功！')
            except ValueError:
                # conn.rollback  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败！')
            conn.close()  # 关闭连接
            file = open('a.txt', 'r+')
            file.seek(0)
            file.truncate()
            file.close()
            file = open('a.txt', 'w+')
            file.write('未选中')
            file.close()


# 查找商品信息
class FindGoodsInformation:
    def __init__(self, subInterface, NAME):
        self.id = '商品编号：' + ' '
        self.name = '商品名称：' + ' '
        self.type = '商品类别：' + ' '
        self.price = '商品价格：' + ' ' + '元'
        self.stock = '商品库存：' + ' '

        # 数据库操作 查询商品信息表
        conn = pymysql.connect(
            host="localhost", port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select * from lgoods where 商品名称 = '%s'" % NAME  # 查询该商品的所有信息
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id = '商品编号：' + row[0]
                self.name = '商品名称: ' + row[1]
                self.type = '商品类别：' + row[2]
                self.price = '商品价格：' + row[3] + '元'
                self.stock = '商品库存：' + row[4]

        except ValueError:
            print("Error: unable to fetch data")
        conn.close()  # 关闭连接
        if NAME == '':
            messagebox.showinfo('警告！', '请输入商品名称！')
        elif self.name == '商品名称：' + ' ':
            messagebox.showinfo('警告！', '找不到该商品！')
        else:
            self.window = tk.Tk()
            self.window.title("查找商品信息")
            screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
            screenheight = self.window.winfo_screenheight()  # 获取屏幕高
            # 使窗口位于屏幕中央
            self.window.geometry(
                '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))
            label = tk.Label(self.window, text='商品信息搜索结果', bg='SkyBlue', font=("宋体", 20), width=70,
                             height=2)
            label.pack(pady=20)
            Label(self.window, text=self.id, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.name, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.type, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.price, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.stock, font=("宋体", 18)).pack(pady=5)
            self.window.mainloop()  # 进入消息循环


# 查找顾客信息
class FindCustomerInformation:
    def __init__(self, subInterface, NAME):
        self.id = '顾客编号：' + ' '
        self.name = '姓名：' + ' '
        self.sex = '性别：' + ' '
        self.num = '联系方式：' + ' '
        self.level = '级别：' + ' '
        self.coupon = '优惠券：' + ' '
        self.data = '注册时间：' + ' '
        self.password = '密码:' + ''

        # 数据库操作 查询顾客信息表
        conn = pymysql.connect(
            host="localhost", port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select * from lcustomer where 姓名 = '%s'" % NAME  # 查询该顾客的所有信息
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id = '顾客编号：' + row[0]
                self.name = '姓名：' + row[1]
                self.sex = '性别：' + row[2]
                self.num = '联系方式：' + row[3]
                self.level = '级别：' + row[4]
                self.coupon = '优惠券：' + row[5]
                self.data = '注册时间：' + row[6]
                self.password = '密码:' + row[7]
        except ValueError:
            print("Error: unable to fetch data")
        conn.close()  # 关闭连接
        if NAME == '':
            messagebox.showinfo('警告！', '请输入姓名！')
        elif self.id == '顾客编号：' + ' ':
            messagebox.showinfo('警告！', '找不到这名顾客！')
        else:
            self.window = tk.Tk()
            self.window.title("查找顾客信息")
            screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
            screenheight = self.window.winfo_screenheight()  # 获取屏幕高
            # 使窗口位于屏幕中央
            self.window.geometry(
                '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))
            label = tk.Label(self.window, text='顾客信息搜索结果', bg='SkyBlue', font=("宋体", 20), width=70,
                             height=2)
            label.pack(pady=20)
            Label(self.window, text=self.id, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.name, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.sex, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.num, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.level, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.coupon, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.data, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.password, font=("宋体", 18)).pack(pady=5)
            self.window.mainloop()  # 进入消息循环


# 查找管理员信息
class FindADInformation:
    def __init__(self, subInterface, ACCOUNT):
        self.account = '账号：' + ' '
        self.password = '密码：' + ' '
        self.remark = '备注：' + ' '

        # 数据库操作 查询管理员信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select * from Lad where 账号 = '%s'" % ACCOUNT  # 查询该账号的所有信息
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.account = '账号：' + row[0]
                self.password = '密码：' + row[1]
                self.remark = '备注：' + row[2]
        except ValueError:
            print("Error: unable to fetch data")
        conn.close()  # 关闭连接
        if ACCOUNT == '':
            messagebox.showinfo('警告！', '请输入账号！')
        elif self.account == '账号：' + ' ':
            messagebox.showinfo('警告！', '找不到这个账号！')
        else:
            self.window = tk.Tk()
            self.window.title("查找管理员信息")
            screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
            screenheight = self.window.winfo_screenheight()  # 获取屏幕高
            # 使窗口位于屏幕中央
            self.window.geometry(
                '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))
            label = tk.Label(self.window, text='管理员信息搜索结果', bg='SkyBlue', font=("宋体", 20), width=70,
                             height=2)
            label.pack(pady=20)
            Label(self.window, text=self.account, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.password, font=("宋体", 18)).pack(pady=5)
            Label(self.window, text=self.remark, font=("宋体", 18)).pack(pady=5)
            self.window.mainloop()  # 进入消息循环


# 添加商品
class AddGoods:
    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title("添加商品界面")
        screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
        screenheight = self.window.winfo_screenheight()  # 获取屏幕高
        # 使窗口位于屏幕中央
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

        self.TopTitle = Label(self.window, text='添加商品', bg='SkyBlue', font=("宋体", 20), width=70, height=2)
        self.TopTitle.pack()

        self.GID = StringVar()  # 声明商品编号
        self.GName = StringVar()  # 声明商品名字
        self.GType = StringVar()  # 声明商品类型
        self.GPrice = StringVar()  # 声明商品价格
        self.GStock = StringVar()  # 声明商品库存
        # 商品编号
        self.rightTopIdLabel = Label(text='商品编号：', font=("宋体", 10))
        self.rightTopIdLabel.pack(pady=10)
        self.rightTopIdEntry = Entry(textvariable=self.GID, font=("宋体", 10))
        self.rightTopIdEntry.pack()
        # 商品名字
        self.rightTopGoodsNameLabel = Label(text='商品名字：', font=("宋体", 10))
        self.rightTopGoodsNameLabel.pack(pady=10)
        self.rightTopGoodsNameEntry = Entry(textvariable=self.GName, font=("宋体", 10))
        self.rightTopGoodsNameEntry.pack()
        # 商品类型
        self.rightTopTypeLabel = Label(text='商品类型：', font=("宋体", 10))
        self.rightTopTypeLabel.pack(pady=10)
        self.rightTopTypeEntry = Entry(textvariable=self.GType, font=("宋体", 10))
        self.rightTopTypeEntry.pack()
        # 商品价格
        self.rightTopPriceLabel = Label(text='商品价格： (单位元)', font=("宋体", 10))
        self.rightTopPriceLabel.pack(pady=10)
        self.rightTopPriceEntry = Entry(textvariable=self.GPrice, font=("宋体", 10))
        self.rightTopPriceEntry.pack()
        # 商品库存
        self.rightTopStockLabel = Label(text='商品库存：', font=("宋体", 10))
        self.rightTopStockLabel.pack(pady=10)
        self.rightTopStockEntry = Entry(textvariable=self.GStock, font=("宋体", 10))
        self.rightTopStockEntry.pack()

        self.rightTopButton1 = ttk.Button(text='确定', width=20, command=self.Add)
        self.rightTopButton1.pack(pady=30)
        self.rightTopButton2 = ttk.Button(text='返回', width=20, command=self.back)
        self.rightTopButton2.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭

        self.id = []
        self.name = []
        self.type = []
        self.price = []
        self.stock = []

        # 数据库操作 查询商品信息表
        conn = pymysql.connect(
            host='127.0.0.1', port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select * from lgoods"  # 查询所有商品信息
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.name.append(row[1])
                self.type.append(row[2])
                self.price.append(row[3])
                self.stock.append(row[4])

        except ValueError:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()  # 关闭连接

    def back(self):
        GoodsInformationOperation(self.window)  # 返回商品信息操作界面

    def Add(self):
        if str(self.GID.get()) in self.id or str(self.GName.get()) in self.name:
            messagebox.showinfo('警告！', '该商品已存在！')
        else:
            if self.GID.get() != '' and self.GName.get() != '' and self.GType.get() != '' and self.GPrice.get() != '' \
                    and self.GStock.get() != '':
                # 数据库操作 查询商品信息表
                conn = pymysql.connect(
                    host="localhost", port=3306,
                    user="root", passwd="123",
                    database='csm', charset='utf8'
                )  # 创建连接
                cursor = conn.cursor()  # 获取游标对象
                sql = "insert into lgoods(商品编号, 商品名称, 商品类别, 商品价格, 商品库存) values ('%s', '%s', '%s', '%s', '%s')" % (
                    self.GID.get(), self.GName.get(), self.GType.get(), self.GPrice.get(),
                    self.GStock.get())  # 向商品信息表插入商品编号, 商品名称, 商品类别, 商品价格, 商品库存等信息
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    conn.commit()
                    messagebox.showinfo('提示！', '插入成功！')
                except ValueError:
                    conn.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()  # 关闭连接


# 添加顾客
class AddReader:
    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title("添加顾客界面")
        screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
        screenheight = self.window.winfo_screenheight()  # 获取屏幕高
        # 使窗口位于屏幕中央
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 650, (screenwidth - 800) / 2, (screenheight - 650) / 2))

        self.TopTitle = Label(self.window, text='添加顾客', bg='SkyBlue', font=("宋体", 20), width=70, height=2)
        self.TopTitle.pack()

        self.CId = StringVar()  # 声明顾客编号
        self.CName = StringVar()  # 声明姓名
        self.CSex = StringVar()  # 声明性别
        self.CNum = StringVar()  # 声明联系方式
        self.CLevel = StringVar()  # 声明级别
        self.CCoupon = StringVar()  # 声明优惠劵
        self.CData = StringVar()  # 声明注册时间
        self.CPassword = StringVar()  # 声明密码
        # 顾客编号
        self.rightTopIdLabel = Label(text='顾客编号：', font=("宋体", 10))
        self.rightTopIdLabel.pack(pady=10)
        self.rightTopIdEntry = Entry(textvariable=self.CId, font=("宋体", 10))
        self.rightTopIdEntry.pack()
        # 姓名
        self.rightTopNameLabel = Label(text='姓名：', font=("宋体", 10))
        self.rightTopNameLabel.pack(pady=10)
        self.rightTopNameEntry = Entry(textvariable=self.CName, font=("宋体", 10))
        self.rightTopNameEntry.pack()
        # 性别
        self.rightTopSexLabel = Label(text='性别：（格式：填‘男’或‘女’）', font=("宋体", 10))
        self.rightTopSexLabel.pack(pady=10)
        self.rightTopSexEntry = Entry(textvariable=self.CSex, font=("宋体", 10))
        self.rightTopSexEntry.pack()
        # 联系方式
        self.rightTopNumLabel = Label(text='联系方式：(格式：电话号码或手机号码)', font=("宋体", 10))
        self.rightTopNumLabel.pack(pady=10)
        self.rightTopNumEntry = Entry(textvariable=self.CNum, font=("宋体", 10))
        self.rightTopNumEntry.pack()
        # 级别
        self.rightTopLevelLabel = Label(text='级别：', font=("宋体", 10))
        self.rightTopLevelLabel.pack(pady=10)
        self.rightTopLevelEntry = Entry(textvariable=self.CLevel, font=("宋体", 10))
        self.rightTopLevelEntry.pack()

        self.rightTopCouponLabel = Label(text='优惠劵：', font=("宋体", 10))
        self.rightTopCouponLabel.pack(pady=10)
        self.rightTopCouponEntry = Entry(textvariable=self.CCoupon, font=("宋体", 10))
        self.rightTopCouponEntry.pack()

        self.rightTopDataLabel = Label(text='注册时间：', font=("宋体", 10))
        self.rightTopDataLabel.pack(pady=10)
        self.rightTopDataEntry = Entry(textvariable=self.CData, font=("宋体", 10))
        self.rightTopDataEntry.pack()
        self.rightTopDataLabel = Label(text='密码：', font=("宋体", 10))
        self.rightTopDataLabel.pack(pady=10)
        self.rightTopDataEntry = Entry(textvariable=self.CPassword, font=("宋体", 10))
        self.rightTopDataEntry.pack()

        self.rightTopButton1 = ttk.Button(text='确定', width=20, command=self.Add)
        self.rightTopButton1.pack(pady=30)
        self.rightTopButton2 = ttk.Button(text='返回', width=20, command=self.back)
        self.rightTopButton2.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭

        self.id = []
        self.name = []
        self.sex = []
        self.num = []
        self.level = []
        self.coupon = []
        self.data = []
        self.password = []
        # 数据库操作 查询顾客信息表
        conn = pymysql.connect(
            host="localhost", port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select * from lcustomer"  # 查询所有顾客信息
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.name.append(row[1])
                self.sex.append(row[2])
                self.num.append(row[3])
                self.level.append(row[4])
                self.coupon.append(row[5])
                self.data.append(row[6])
                self.password.append(row[7])
        except ValueError:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()  # 关闭连接

    def back(self):
        CustomerInformationOperation(self.window)  # 返回顾客信息操作界面

    def Add(self):
        if str(self.CId.get()) in self.id:
            messagebox.showinfo('警告！', '该顾客已存在！')
        else:
            if self.CId.get() != '' and self.CName.get() != '' and self.CSex.get() != '' and self.CNum.get() != '' \
                    and self.CLevel.get() != '' and self.CCoupon.get() != '' and self.CData.get() != '' and self.CPassword.get() != '':
                # 数据库操作 查询顾客信息表
                conn = pymysql.connect(
                    host="localhost", port=3306,
                    user="root", passwd="123",
                    database='csm', charset='utf8'
                )  # 创建连接
                cursor = conn.cursor()  # 获取游标对象
                sql_0 = "insert into lcustomer(顾客编号, 姓名, 性别, 联系方式, 级别, 优惠劵, 注册时间, 密码)values" \
                        "('%s', '%s', '%s', '%s', '%s', '%s','%s','%s')"
                sql = sql_0 % (self.CId.get(), self.CName.get(), self.CSex.get(), self.CNum.get(), self.CLevel.get(),
                               self.CCoupon.get(), self.CData.get(),
                               self.CPassword.get())  # 向顾客信息表插入顾客编号, 姓名, 性别, 联系方式, 级别, 优惠劵, 注册时间，密码等信息
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    conn.commit()
                    messagebox.showinfo('提示！', '插入成功！')
                except ValueError:
                    conn.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()  # 关闭连接


# 添加管理员
class AddAD:
    def __init__(self, subInterface):
        subInterface.destroy()
        self.window = tk.Tk()
        self.window.title("添加管理员界面")
        screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
        screenheight = self.window.winfo_screenheight()  # 获取屏幕高
        # 使窗口位于屏幕中央
        self.window.geometry(
            '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

        self.TopTitle = Label(self.window, text='添加管理员', bg='SkyBlue', font=("宋体", 20), width=70, height=2)
        self.TopTitle.pack()

        self.varAccount = StringVar()  # 声明账号
        self.varPassword = StringVar()  # 声明密码
        self.varRemark = StringVar()  # 声明备注
        # 账号
        self.rightTopAccountLabel = Label(text='账号：', font=("宋体", 10))
        self.rightTopAccountLabel.pack(pady=10)
        self.rightTopAccountEntry = Entry(textvariable=self.varAccount, font=("宋体", 10))
        self.rightTopAccountEntry.pack()
        # 密码
        self.rightTopPasswordLabel = Label(text='密码：', font=("宋体", 10))
        self.rightTopPasswordLabel.pack(pady=10)
        self.rightTopPasswordEntry = Entry(textvariable=self.varPassword, font=("宋体", 10))
        self.rightTopPasswordEntry.pack()

        self.rightTopButton1 = ttk.Button(text='确定', width=20, command=self.Add)
        self.rightTopButton1.pack(pady=15)
        self.rightTopButton2 = ttk.Button(text='返回', width=20, command=self.back)
        self.rightTopButton2.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭

        self.account = []
        self.password = []
        self.remark = []
        # 数据库操作 查询管理员信息表
        conn = pymysql.connect(
            host="localhost", port=3306,
            user="root", passwd="123",
            database='csm', charset='utf8'
        )  # 创建连接
        cursor = conn.cursor()  # 获取游标对象
        sql = "select * from Lad"  # 查询所有管理员信息
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.account.append(row[0])
                self.password.append(row[1])
                self.remark.append(row[2])
        except ValueError:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        conn.close()  # 关闭连接

    def back(self):
        ADInformationOperation(self.window)  # 返回管理员信息操作界面

    def Add(self):
        if str(self.varAccount.get()) in self.account:
            messagebox.showinfo('警告！', '该管理员已存在！')
        else:
            if self.varAccount.get() != '' and self.varPassword.get() != '':
                # 数据库操作 查询管理员信息表
                conn = pymysql.connect(
                    host="localhost", port=3306,
                    user="root", passwd="123",
                    database='csm', charset='utf8'
                )  # 创建连接
                cursor = conn.cursor()  # 获取游标对象
                sql = "insert into Lad(账号, 密码, 备注) values ('%s', '%s', '%s')" % (
                    self.varAccount.get(), self.varPassword.get(), '普通管理员')  # 向管理员信息表插入账号, 密码, 备注等信息
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    conn.commit()
                    messagebox.showinfo('提示！', '插入成功！')
                except ValueError:
                    conn.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()  # 关闭连接


# 修改商品信息
class EditGoodsInformation:
    def __init__(self, subInterface):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请先选中一条商品信息')
        else:
            subInterface.destroy()
            self.window = tk.Tk()
            self.window.title("修改商品信息界面")
            screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
            screenheight = self.window.winfo_screenheight()  # 获取屏幕高
            # 使窗口位于屏幕中央
            self.window.geometry(
                '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

            self.topTitle = Label(self.window, text='输入新的商品信息', bg='SkyBlue', font=("宋体", 20), width=70,
                                  height=2)
            self.topTitle.pack()

            self.GID = StringVar()  # 声明商品编号
            self.GName = StringVar()  # 声明商品名字
            self.GType = StringVar()  # 声明商品类别
            self.GPrice = StringVar()  # 声明商品价格
            self.GStock = StringVar()  # 声明商品库存

            # 商品编号
            self.idLabel = Label(text='商品编号（不可修改）:', font=("宋体", 10))
            self.idLabel.pack(pady=10)
            self.idEntry = Entry(textvariable=self.GID, font=("宋体", 10))
            self.idEntry.pack()
            # 商品名字
            self.nameLabel = Label(text='商品名字：', font=("宋体", 10))
            self.nameLabel.pack(pady=10)
            self.nameEntry = Entry(textvariable=self.GName, font=("宋体", 10))
            self.nameEntry.pack()
            # 商品类别
            self.typeLabel = Label(text='商品类别：', font=("宋体", 10))
            self.typeLabel.pack(pady=10)
            self.typeEntry = Entry(textvariable=self.GType, font=("宋体", 10))
            self.typeEntry.pack()
            # 商品价格
            self.priceLabel = Label(text='商品价格：(单位元)', font=("宋体", 10))
            self.priceLabel.pack(pady=10)
            self.priceEntry = Entry(textvariable=self.GPrice, font=("宋体", 10))
            self.priceEntry.pack()
            # 商品库存
            self.stockLabel = Label(text='商品库存：', font=("宋体", 10))
            self.stockLabel.pack(pady=10)
            self.stockEntry = Entry(textvariable=self.GStock, font=("宋体", 10))
            self.stockEntry.pack()

            self.button1 = ttk.Button(text='确定', width=20, command=self.update)
            self.button1.pack(pady=30)
            self.button2 = ttk.Button(text='返回', width=20, command=self.back)
            self.button2.pack()
            self.window.protocol('WM_DELETE_WINDOW', self.back)  # 捕捉右上角关闭点击

    def back(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()
        GoodsInformationOperation(self.window)  # 返回商品操作界面

    def update(self):
        self.id = StringVar()
        file = open('a.txt', 'r')
        self.id = file.read()
        file.close()
        prompt = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if prompt is True:
            if self.GID.get() == self.id and self.GID.get() != '' and self.GName.get() != '' \
                    and self.GType.get() != '' and self.GPrice.get() != '' and self.GStock.get() != '':
                # 数据库操作 查询商品信息表
                conn = pymysql.connect(
                    host="localhost", port=3306,
                    user="root", passwd="123",
                    database='csm', charset='utf8'
                )  # 创建连接
                cursor = conn.cursor()  # 获取游标对象
                sql_0 = "update lgoods set 商品名称 = '%s', 商品类别 = '%s', 商品价格 = '%s', 商品库存 = '%s' where 商品编号 = '%s'"
                sql = sql_0 % (self.GName.get(), self.GType.get(), self.GPrice.get(), self.GStock.get(),
                               self.GID.get())  # 修改商品信息表中对应商品编号的商品名称，商品类型，商品价格，商品库存等信息
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    conn.commit()
                    messagebox.showinfo('提示！', '更新成功！')
                except ValueError:
                    conn.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()  # 关闭连接
            else:
                messagebox.showinfo('警告！', '商品编号不可修改且输入完整数据！')


# 修改顾客信息
class EditCustomerInformation:
    def __init__(self, subInterface):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请先选中一条顾客信息')
        else:
            subInterface.destroy()
            self.window = tk.Tk()
            self.window.title("修改顾客信息界面")
            screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
            screenheight = self.window.winfo_screenheight()  # 获取屏幕高
            # 使窗口位于屏幕中央
            self.window.geometry(
                '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

            self.topTitle = Label(self.window, text='输入新的顾客信息', bg='SkyBlue', font=("宋体", 20), width=70,
                                  height=2)
            self.topTitle.pack()

            self.CId = StringVar()  # 声明顾客编号
            self.CName = StringVar()  # 声明姓名
            self.CSex = StringVar()  # 声明性别
            self.CNum = StringVar()  # 声明联系方式
            self.CLevel = StringVar()  # 声明级别
            self.CCoupon = StringVar()  # 声明优惠劵
            self.CData = StringVar()  # 声明注册时间

            # 顾客编号
            self.idLabel = Label(text='顾客编号（不可修改）：', font=("宋体", 10))
            self.idLabel.pack(pady=10)
            self.idEntry = Entry(textvariable=self.CId, font=("宋体", 10))
            self.idEntry.pack()
            # 姓名
            self.nameLabel = Label(text='姓名：', font=("宋体", 10))
            self.nameLabel.pack(pady=10)
            self.nameEntry = Entry(textvariable=self.CName, font=("宋体", 10))
            self.nameEntry.pack()
            # 性别
            self.sexLabel = Label(text='性别：', font=("宋体", 10))
            self.sexLabel.pack(pady=10)
            self.sexEntry = Entry(textvariable=self.CSex, font=("宋体", 10))
            self.sexEntry.pack()
            # 联系方式
            self.numLabel = Label(text='联系方式：(格式：电话号码或手机号码)', font=("宋体", 10))
            self.numLabel.pack(pady=10)
            self.numEntry = Entry(textvariable=self.CNum, font=("宋体", 10))
            self.numEntry.pack()
            # 级别
            self.levelLabel = Label(text='级别：', font=("宋体", 10))
            self.levelLabel.pack(pady=10)
            self.levelEntry = Entry(textvariable=self.CLevel, font=("宋体", 10))
            self.levelEntry.pack()
            # 优惠劵
            self.couponLabel = Label(text='优惠劵：', font=("宋体", 10))
            self.couponLabel.pack(pady=10)
            self.couponEntry = Entry(textvariable=self.CCoupon, font=("宋体", 10))
            self.couponEntry.pack()
            # 注册时间
            self.dataLabel = Label(text='注册时间：', font=("宋体", 10))
            self.dataLabel.pack(pady=10)
            self.dataEntry = Entry(textvariable=self.CData, font=("宋体", 10))
            self.dataEntry.pack()

            self.button1 = ttk.Button(text='确定', width=20, command=self.update)
            self.button1.pack(pady=30)
            self.button2 = ttk.Button(text='返回', width=20, command=self.back)
            self.button2.pack()
            self.window.protocol('WM_DELETE_WINDOW', self.back)  # 捕捉右上角关闭点击

    def back(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()
        CustomerInformationOperation(self.window)  # 返回顾客操作界面

    def update(self):
        self.id = StringVar()
        file = open('a.txt', 'r')
        self.id = file.read()
        file.close()
        prompt = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if prompt is True:
            if self.CId.get() == self.id and self.CId.get() != '' and self.CName.get() != '' and self.CSex.get() != '' \
                    and self.CNum.get() != '' and self.CLevel.get() != '' and self.CCoupon.get() != '' \
                    and self.CData.get() != '':
                # 数据库操作 查询顾客信息表
                conn = pymysql.connect(
                    host="localhost", port=3306,
                    user="root", passwd="123",
                    database='csm', charset='utf8'
                )  # 创建连接
                cursor = conn.cursor()  # 获取游标对象
                sql = "update lcustomer set 姓名 = '%s', 性别 = '%s', 联系方式 = '%s', 级别 = '%s', 优惠劵 = '%s', 注册时间" \
                      " = '%s' where 顾客编号 = '%s'" % \
                      (self.CName.get(), self.CSex.get(), self.CNum.get(), self.CLevel.get(), self.CCoupon.get(),
                       self.CData.get(), self.CId.get())  # 修改顾客信息表中对应顾客编号的姓名，性别，联系方式，级别等信息
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    conn.commit()
                    messagebox.showinfo('提示！', '更新成功！')
                except ValueError:
                    conn.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()  # 关闭连接
            else:
                messagebox.showinfo('警告！', '顾客编号不可修改且输入完整数据！')


# 修改管理员信息
class EditADInformation:
    def __init__(self, subInterface):
        file = open('a.txt', 'r')
        inspection = file.read()
        file.close()
        if inspection == '未选中':
            messagebox.showinfo('警告！', '请先选中一条管理员信息')
        else:
            subInterface.destroy()
            self.window = tk.Tk()
            self.window.title("修改管理员信息界面")
            screenwidth = self.window.winfo_screenwidth()  # 获取屏幕宽
            screenheight = self.window.winfo_screenheight()  # 获取屏幕高
            # 使窗口位于屏幕中央
            self.window.geometry(
                '%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2))

            self.topTitle = Label(self.window, text='输入新的密码', bg='SkyBlue', font=("宋体", 20), width=70,
                                  height=2)
            self.topTitle.pack()

            self.varPassword = StringVar()  # 声明密码

            # 密码
            self.passwordLabel = Label(text='密码：（格式：不可超过16位）', font=("宋体", 10))
            self.passwordLabel.pack(pady=10)
            self.passwordEntry = Entry(textvariable=self.varPassword, font=("宋体", 10))
            self.passwordEntry.pack()

            self.button1 = ttk.Button(text='确定', width=20, command=self.update)
            self.button1.pack(pady=30)
            self.button2 = ttk.Button(text='返回', width=20, command=self.back)
            self.button2.pack()
            self.window.protocol('WM_DELETE_WINDOW', self.back)  # 捕捉右上角关闭点击

    def back(self):
        file = open('a.txt', 'r+')
        file.seek(0)
        file.truncate()
        file.close()
        file = open('a.txt', 'w+')
        file.write('未选中')
        file.close()
        ADInformationOperation(self.window)  # 返回管理员操作界面

    def update(self):
        self.account = StringVar()
        file = open('a.txt', 'r')
        self.account = file.read()
        file.close()
        prompt = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if prompt is True:
            if self.varPassword.get() != '':
                # 数据库操作 查询管理员信息表
                conn = pymysql.connect(
                    host="localhost", port=3306,
                    user="root", passwd="123",
                    database='csm', charset='utf8'
                )  # 创建连接
                cursor = conn.cursor()  # 获取游标对象
                sql = "update Lad set 密码 = '%s' where 账号 = '%s'" % (
                    self.varPassword.get(), self.account)  # 修改管理员信息表中对应账号的密码
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    conn.commit()
                    messagebox.showinfo('提示！', '更新成功！')
                except ValueError:
                    conn.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                conn.close()  # 关闭连接
            else:
                messagebox.showinfo('警告！', '请输入新的密码！')


def main():
    window = tk.Tk()
    MainInterface(window)


if __name__ == '__main__':
    faceCascade = cv2.CascadeClassifier(
        f'cascades/haarcascade_frontalface_default.xml')
    main()
