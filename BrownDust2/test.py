
## 获取活动窗口
import pyautogui



allWindows = pyautogui.getAllWindows()
print(allWindows)
## 打印所有活动窗口
for win32Window in allWindows:
    print("打印所有活动窗口:",win32Window)
 
## 获取 所有标题 
## ['开始', '', 'windows_gui_test.py - python_work - Visual Studio Code', 'Program Manager', '']
allTitles = pyautogui.getAllTitles()
print(allTitles)
## 打印所有活动标题
for title in allTitles:
    print("打印所有活动标题:{0}".format(title))