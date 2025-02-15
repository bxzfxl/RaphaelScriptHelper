"""
场景配置文件
定义游戏中的各种场景及其处理方式
"""

import cv2
import mss
import time
import logging
import pydirectinput
import numpy as np
from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, Callable, Optional, Tuple
from brownDust2Dict import *
from utils import click_random, show_message_dialog

class Config:
    """全局配置类"""
    # 元素识别置信度配置
    CONFIDENCE = {
        'mainline': 0.7,    # 主线按钮
        'skip': 0.7,        # 跳过按钮
        'skipChat': 0.8,    # 对话跳过
        'exit': 0.8,        # 退出按钮
        'autoMove': 0.8,    # 自动移动
        'inter': 0.85,      # 交互按钮
        'war': 0.7,         # 战斗状态
        'confirm': 0.7,     # 确认按钮
        'pause': 0.8,       # 暂停标志
    }
    
    # 场景匹配配置
    SCENE_MATCH = {
        'mainline': {
            'confidence': {'mainline': 0.7, 'inter': 0.85},
            'required': {'mainline': True, 'inter': False, 'pause': False}
        },
        'interaction': {
            'confidence': {'mainline': 0.7, 'inter': 0.85},
            'required': {'mainline': True, 'inter': True}
        },
        'dialogue': {
            'confidence': {'skip': 0.7, 'mainline': 0.7},
            'required': {'skip': True, 'mainline': False}
        },
        'deep_dialogue': {
            'confidence': {'skipChat': 0.8},
            'required': {'skipChat': True}
        },
        'battle': {
            'confidence': {'war': 0.7},
            'required': {'war': True}
        },
        'battle_end': {
            'confidence': {'exit': 0.8},
            'required': {'exit': True}
        },
        'confirm': {
            'confidence': {'confirm': 0.7},
            'required': {'confirm': True}
        },
        'automove': {
            'confidence': {'autoMove': 0.8},
            'required': {'autoMove': True}
        },
        'pause': {
            'confidence': {'pause': 0.8},
            'required': {'pause': True}
        }
    }

class Scene(Enum):
    """游戏场景枚举"""
    MAINLINE = auto()      # 主线入口
    INTERACTION = auto()    # 交互场景
    DIALOGUE = auto()      # 对话场景
    DEEP_DIALOGUE = auto() # 深入对话
    BATTLE = auto()        # 战斗中
    BATTLE_END = auto()    # 战斗结束
    CONFIRM = auto()       # 确认场景
    AUTOMOVE = auto()      # 自动移动
    PAUSE = auto()         # 人工介入
    UNKNOWN = auto()       # 未知场景

@dataclass
class ScenePattern:
    """场景特征模式"""
    elements: Dict[str, float]       # 需要检测的元素及其置信度
    required_matches: Dict[str, bool] # 元素是否必须存在

@dataclass
class SceneConfig:
    """场景配置"""
    pattern: ScenePattern    # 场景匹配模式
    handler: Callable        # 场景处理函数
    description: str         # 场景描述

def handle_mainline(manager) -> None:
    """处理主线场景"""
    from utils import click_random  # 避免循环导入
    click_random(mainLine_click)
    time.sleep(2)

def handle_interaction(manager) -> None:
    """处理交互场景"""
    pydirectinput.press('f')
    time.sleep(1)

def handle_dialogue(manager) -> None:
    """处理对话场景"""
    pydirectinput.press('f2')
    time.sleep(1)
    pydirectinput.press('enter')

def handle_deep_dialogue(manager) -> None:
    """处理深入对话场景"""
    pydirectinput.press('enter')
    time.sleep(0.5)

def handle_battle(manager) -> None:
    """处理战斗场景"""
    logging.info("战斗场景，等待中...")
    time.sleep(2)

def handle_battle_end(manager) -> None:
    """处理战斗结束场景"""
    pydirectinput.press('enter')
    time.sleep(1)

def handle_confirm(manager) -> None:
    """处理确认场景"""
    pydirectinput.press('enter')
    time.sleep(1)

def handle_automove(manager) -> None:
    """处理自动移动场景"""
    logging.info("检测到自动移动，等待中...")
    time.sleep(2)

def handle_pause(manager) -> None:
    """处理暂停场景"""
    if not manager.manual_intervention_needed:
        logging.warning("⚠ 检测到需要人工介入")
        manager.manual_intervention_needed = True
        manager.show_intervention_dialog()
    time.sleep(1)

# 场景配置字典
SCENE_CONFIGS = {
    Scene.MAINLINE: SceneConfig(
        pattern=ScenePattern(
            elements=Config.SCENE_MATCH['mainline']['confidence'],
            required_matches=Config.SCENE_MATCH['mainline']['required']
        ),
        handler=handle_mainline,
        description="主线入口场景"
    ),
    
    Scene.INTERACTION: SceneConfig(
        pattern=ScenePattern(
            elements=Config.SCENE_MATCH['interaction']['confidence'],
            required_matches=Config.SCENE_MATCH['interaction']['required']
        ),
        handler=handle_interaction,
        description="交互场景"
    ),
    
    Scene.DIALOGUE: SceneConfig(
        pattern=ScenePattern(
            elements=Config.SCENE_MATCH['dialogue']['confidence'],
            required_matches=Config.SCENE_MATCH['dialogue']['required']
        ),
        handler=handle_dialogue,
        description="对话场景"
    ),
    
    Scene.DEEP_DIALOGUE: SceneConfig(
        pattern=ScenePattern(
            elements=Config.SCENE_MATCH['deep_dialogue']['confidence'],
            required_matches=Config.SCENE_MATCH['deep_dialogue']['required']
        ),
        handler=handle_deep_dialogue,
        description="深入对话场景"
    ),
    
    Scene.BATTLE: SceneConfig(
        pattern=ScenePattern(
            elements=Config.SCENE_MATCH['battle']['confidence'],
            required_matches=Config.SCENE_MATCH['battle']['required']
        ),
        handler=handle_battle,
        description="战斗场景"
    ),
    
    Scene.BATTLE_END: SceneConfig(
        pattern=ScenePattern(
            elements=Config.SCENE_MATCH['battle_end']['confidence'],
            required_matches=Config.SCENE_MATCH['battle_end']['required']
        ),
        handler=handle_battle_end,
        description="战斗结束场景"
    ),
    
    Scene.CONFIRM: SceneConfig(
        pattern=ScenePattern(
            elements=Config.SCENE_MATCH['confirm']['confidence'],
            required_matches=Config.SCENE_MATCH['confirm']['required']
        ),
        handler=handle_confirm,
        description="确认场景"
    ),
    
    Scene.AUTOMOVE: SceneConfig(
        pattern=ScenePattern(
            elements=Config.SCENE_MATCH['automove']['confidence'],
            required_matches=Config.SCENE_MATCH['automove']['required']
        ),
        handler=handle_automove,
        description="自动移动场景"
    ),
    
    Scene.PAUSE: SceneConfig(
        pattern=ScenePattern(
            elements=Config.SCENE_MATCH['pause']['confidence'],
            required_matches=Config.SCENE_MATCH['pause']['required']
        ),
        handler=handle_pause,
        description="暂停场景"
    )
}

def get_scene_elements() -> Dict[str, tuple]:
    """获取所有需要检测的场景元素"""
    return {
        'mainline': (mainline, mainline_pos),
        'skip': (skip, skip_pos),
        'inter': (inter, inter_pos),
        'skipChat': (skipchat, skipchat_pos),
        'war': (war, war_pos),
        'exit': (exit, exit_pos),
        'autoMove': (automove, automove_pos),
        'pause': (pause, pause_pos),
    } 

class SceneManager:
    """场景管理器：负责识别和处理不同的游戏场景"""
    
    def __init__(self):
        self.sct = mss.mss()
        self.screen_size = None
        self.reset_state()

    def reset_state(self):
        """重置所有状态变量"""
        self.current_scene = Scene.UNKNOWN
        self.element_positions = {}
        self.manual_intervention_needed = False
        self.script_running = False  # 默认暂停状态

    def get_screen_size(self) -> Tuple[int, int]:
        """获取并缓存屏幕尺寸"""
        if not self.screen_size:
            monitor = self.sct.monitors[1]
            self.screen_size = (monitor['width'], monitor['height'])
        return self.screen_size

    def get_roi_from_relative_pos(self, rel_pos: dict) -> tuple:
        """
        根据相对位置信息计算实际的ROI区域
        
        参数:
            rel_pos: 包含相对位置信息的字典 {'x0':float, 'y0':float, 'x1':float, 'y1':float}
            
        返回:
            (x0, y0, x1, y1) 实际像素坐标
        """
        if not self.screen_size:
            self.get_screen_size()
        
        w, h = self.screen_size
        x0 = int(rel_pos['x0'] * w)
        y0 = int(rel_pos['y0'] * h)
        x1 = int(rel_pos['x1'] * w)
        y1 = int(rel_pos['y1'] * h)
        
        # 添加边界余量
        margin_x = int((x1 - x0) * 0.1)
        margin_y = int((y1 - y0) * 0.1)
        
        x0 = max(0, x0 - margin_x)
        y0 = max(0, y0 - margin_y)
        x1 = min(w, x1 + margin_x)
        y1 = min(h, y1 + margin_y)
        
        return (x0, y0, x1, y1)

    def check_image(self, target: str, confidence: float, rel_pos: dict = None) -> Optional[Tuple[int, int]]:
        """检查目标图像是否存在于当前屏幕"""
        try:
            monitor = self.sct.monitors[1]
            
            if rel_pos:
                x0, y0, x1, y1 = self.get_roi_from_relative_pos(rel_pos)
                monitor = {
                    'left': monitor['left'] + x0,
                    'top': monitor['top'] + y0,
                    'width': x1 - x0,
                    'height': y1 - y0
                }
            
            sct_img = self.sct.grab(monitor)
            img = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGRA2BGR)
            
            template = cv2.imread(target)
            if template is None:
                raise FileNotFoundError(f"模板文件不存在: {target}")
            
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            
            if max_val > confidence:
                h, w = template.shape[:2]
                if rel_pos:
                    center_x = max_loc[0] + w//2 + x0
                    center_y = max_loc[1] + h//2 + y0
                else:
                    center_x = max_loc[0] + w//2
                    center_y = max_loc[1] + h//2
                    
                logging.info(f"成功识别 {target[17:]} 置信度:{max_val:.2f} 坐标({center_x},{center_y})")
                return (center_x, center_y)
                
            logging.debug(f"未识别到目标 {target[17:]} 置信度:{max_val:.2f}")
            return None
            
        except Exception as e:
            logging.error(f"图像识别异常: {str(e)}")
            return None

    def identify_scene(self) -> Scene:
        """识别当前游戏场景"""
        detected_elements = {}
        
        for element_name, (image_path, pos_info) in get_scene_elements().items():
            result = self.check_image(
                image_path, 
                Config.CONFIDENCE[element_name],  # 使用全局配置的置信度
                pos_info
            )
            detected_elements[element_name] = bool(result)
            if result:
                self.element_positions[element_name] = result

        for scene, config in SCENE_CONFIGS.items():
            matches = True
            for element, required in config.pattern.required_matches.items():
                if required != detected_elements.get(element, False):
                    matches = False
                    break
            if matches:
                return scene

        return Scene.UNKNOWN

    def handle_scene(self, scene: Scene):
        """处理特定场景的操作"""
        config = SCENE_CONFIGS.get(scene)
        if config:
            logging.info(f"处理场景: {config.description}")
            config.handler(self)
        else:
            logging.warning(f"未知场景: {scene}")

    def show_intervention_dialog(self):
        """显示需要人工介入的提示窗口"""
        show_message_dialog(
            "需要人工介入",
            "检测到需要人工操作。\n完成后请按Home键继续运行脚本。"
        ) 