"""
工具函数模块
提供通用的工具函数和辅助功能
"""

import time
import logging
import numpy as np
import pyautogui
import pydirectinput
import keyboard
import tkinter.messagebox
from typing import Tuple

def click_random(pos_area: Tuple[Tuple[int, int], Tuple[int, int]]):
    """
    在指定区域内随机点击
    
    参数:
        pos_area: 包含两个坐标点的区域范围 ((x1,y1), (x2,y2))
    """
    (x1, y1), (x2, y2) = pos_area
    x = np.random.randint(x1, x2)
    y = np.random.randint(y1, y2)
    logging.info(f"随机点击坐标 X:{x} Y:{y}")
    safe_click(x, y)

def safe_click(x: int, y: int, delay: float = 0.5):
    """
    安全的点击操作，包含异常处理和延迟
    
    参数:
        x: 点击位置的X坐标
        y: 点击位置的Y坐标
        delay: 点击后的延迟时间（秒）
    """
    try:
        pyautogui.click(x, y)
        time.sleep(delay)
    except Exception as e:
        logging.error(f"点击操作失败: {e}")

def setup_keyboard_control(manager):
    """
    设置键盘控制
    
    参数:
        manager: 场景管理器实例
    """
    def on_home():
        if manager.manual_intervention_needed:
            manager.manual_intervention_needed = False
            logging.info("✓ 人工介入完成")
        else:
            manager.script_running = True
            logging.info("▶ 脚本开始运行")

    def on_end():
        manager.script_running = False
        logging.info("⏸ 脚本已暂停")

    keyboard.on_press_key('home', lambda _: on_home())
    keyboard.on_press_key('end', lambda _: on_end())

def show_message_dialog(title: str, message: str):
    """
    显示消息对话框
    
    参数:
        title: 对话框标题
        message: 对话框消息内容
    """
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showwarning(title, message)
    root.destroy() 