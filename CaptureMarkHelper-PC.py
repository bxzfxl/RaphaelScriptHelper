# 标点截取工具 Author By Hanmin 2022.01
# 修改版：PC截图版本 By 助手
# 请先安装依赖：pip install mss opencv-python

import cv2
import tkinter
import os
import tkinter.simpledialog
from mss import mss

# 修改以下参数来运行

# 原图缩放比例，用于展示在窗口里
scale = 0.5

# 截图保存路径，以/结束（确保路径已存在）
save_file_path = "./img/"

# py变量字典文件
pos_img_dict = "./testDict.py"

# 动作类型 1=截图  2=标点  3=标线（取起终点组成向量） 4=标记区域
action = 4

# ===================================================
# PC截图功能
def capture_pc_screen(output_filename):
    with mss() as sct:
        # 获取最大分辨率显示器
        monitor = sct.monitors[1]  # 主显示器
        sct_img = sct.grab(monitor)
        
        # 转换为PNG并保存
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_filename)
        return output_filename

# 执行截图（保存为screen.png）
img_file = "./screen.png"
capture_pc_screen(img_file)

# ===================================================
# 以下部分保持原逻辑

def isVarExist(varName):
    if os.path.exists(pos_img_dict):
        with open(pos_img_dict, 'r', encoding='utf-8') as f:
            content = f.read()
            return varName in content
    return False

def createVar(varName, value, type):
    with open(pos_img_dict, 'a+', encoding='utf-8') as f:
        if type == 1:
            f.write(f"{varName} = \"{value}\"\n")
        else:
            f.write(f"{varName} = {value}\n")

def draw_Rect(event, x, y, flags, param):
    global drawing, startPos, stopPos
    if event == cv2.EVENT_LBUTTONDOWN:  # 响应鼠标按下
        drawing = True
        startPos = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:  # 响应鼠标移动
        if drawing == True:
            img = img_source.copy()
            cv2.rectangle(img, startPos, (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img)
    elif event == cv2.EVENT_LBUTTONUP:  # 响应鼠标松开
        drawing = False
        stopPos = (x, y)
    elif event == cv2.EVENT_RBUTTONUP:
        if startPos == (0, 0) and stopPos == (0, 0):
            return
        x0, y0 = startPos
        x1, y1 = stopPos
        cropped = img_source[y0:y1, x0:x1]  # 裁剪坐标为[y0:y1, x0:x1]
        res = tkinter.simpledialog.askstring(title="输入", prompt="请输入图片变量名：（存储路径为" + save_file_path + "）",
                                             initialvalue="")
        if res is not None:
            if isVarExist(res):
                tkinter.simpledialog.messagebox.showerror("错误", "该变量名已存在，请更换一个或手动去文件中删除！")
            else:
                cv2.imwrite(save_file_path + res + ".png", cropped)
                createVar(res, save_file_path + res + ".png", 1)
                tkinter.simpledialog.messagebox.showinfo("提示", "创建完成！")
    elif event == cv2.EVENT_MBUTTONUP:
        if startPos == (0, 0) and stopPos == (0, 0):
            return
        x0, y0 = startPos
        x1, y1 = stopPos
        cropped = img_source[y0:y1, x0:x1]  # 裁剪坐标为[y0:y1, x0:x1]
        cv2.imshow('cropImage', cropped)
        cv2.waitKey(0)


def draw_Point(event, x, y, flags, param):
    global drawing, startPos, stopPos
    if event == cv2.EVENT_LBUTTONDOWN:  # 响应鼠标按下
        drawing = True
        startPos = (x, y)
        img = img_source.copy()
        cv2.circle(img, startPos, 2, (0, 255, 0), 2)
        cv2.putText(img, "Point:" + str(startPos), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
        print("Point:" + str(startPos))
        cv2.imshow('image', img)
    elif event == cv2.EVENT_RBUTTONUP:
        if startPos == (0, 0):
            return
        res = tkinter.simpledialog.askstring(title="输入", prompt="请输入坐标 " + str(startPos) + " 变量名：", initialvalue="")
        if res is not None:
            if isVarExist(res):
                tkinter.simpledialog.messagebox.showerror("错误", "该变量名已存在，请更换一个或手动去文件中删除！")
            else:
                createVar(res, startPos, 2)
                tkinter.simpledialog.messagebox.showinfo("提示", "创建完成！")


def draw_Line(event, x, y, flags, param):
    global drawing, startPos, stopPos
    if event == cv2.EVENT_LBUTTONDOWN:  # 响应鼠标按下
        drawing = True
        startPos = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:  # 响应鼠标移动
        if drawing == True:
            img = img_source.copy()
            cv2.line(img, startPos, (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img)
    elif event == cv2.EVENT_LBUTTONUP:  # 响应鼠标松开
        drawing = False
        stopPos = (x, y)
        print("startPoint:" + str(startPos) + " stopPoint:" + str(stopPos))
    elif event == cv2.EVENT_RBUTTONUP:
        if startPos == (0, 0) and stopPos == (0, 0):
            return
        res = tkinter.simpledialog.askstring(title="输入", prompt="请输入开始坐标 " + str(startPos) + " 到结束坐标 " + str(
            stopPos) + " 组成向量的变量名：", initialvalue="")
        if res is not None:
            if isVarExist(res):
                tkinter.simpledialog.messagebox.showerror("错误", "该变量名已存在，请更换一个或手动去文件中删除！")
            else:
                createVar(res, (startPos, stopPos), 3)
                tkinter.simpledialog.messagebox.showinfo("提示", "创建完成！")


def draw_Rect_Pos(event, x, y, flags, param):
    global drawing, startPos, stopPos
    if event == cv2.EVENT_LBUTTONDOWN:  # 响应鼠标按下
        drawing = True
        startPos = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:  # 响应鼠标移动
        if drawing == True:
            img = img_source.copy()
            cv2.rectangle(img, startPos, (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img)
    elif event == cv2.EVENT_LBUTTONUP:  # 响应鼠标松开
        drawing = False
        stopPos = (x, y)
        print("startPoint:" + str(startPos) + " stopPoint:" + str(stopPos))
    elif event == cv2.EVENT_RBUTTONUP:
        if startPos == (0, 0) and stopPos == (0, 0):
            return
        x0, y0 = startPos
        x1, y1 = stopPos
        res = tkinter.simpledialog.askstring(title="输入", prompt="请输入矩形范围变量名：",
                                             initialvalue="")
        if res is not None:
            if isVarExist(res):
                tkinter.simpledialog.messagebox.showerror("错误", "该变量名已存在，请更换一个或手动去文件中删除！")
            else:
                createVar(res, (startPos, stopPos), 4)
                tkinter.simpledialog.messagebox.showinfo("提示", "创建完成！")
    elif event == cv2.EVENT_MBUTTONUP:
        if startPos == (0, 0) and stopPos == (0, 0):
            return
        x0, y0 = startPos
        x1, y1 = stopPos
        cropped = img_source[y0:y1, x0:x1]  # 裁剪坐标为[y0:y1, x0:x1]
        cv2.imshow('cropImage', cropped)
        cv2.waitKey(0)
   # ===================================================
# 主程序流程
drawing = False
startPos = (0, 0)
stopPos = (0, 0)

try:
    img_source = cv2.imread(img_file)
    if img_source is None:
        raise FileNotFoundError("截图文件生成失败，请检查权限和路径")
except Exception as e:
    tkinter.messagebox.showerror("错误", f"图片加载失败：{str(e)}")
    exit()

h_src, w_src = img_source.shape[:2]
w = int(w_src * scale)
h = int(h_src * scale)

root = tkinter.Tk()
root.title('dialog')
root.resizable(0, 0)
root.withdraw()

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", w, h)

# 设置鼠标回调
mouse_handlers = {
    1: draw_Rect,
    2: draw_Point,
    3: draw_Line,
    4: draw_Rect_Pos
}
cv2.setMouseCallback('image', mouse_handlers.get(action, draw_Rect_Pos))

cv2.imshow('image', img_source)
cv2.waitKey(0)
cv2.destroyAllWindows()
root.destroy()