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
import inspect
from brownDust2Dict import *
from utils import click_random, show_message_dialog

def get_scene_elements() -> Dict[str, tuple]:
    """获取所有需要检测的场景元素"""
    elements = {}
    # 遍历brownDust2Dict中的所有变量，自动收集元素
    for var_name, value in globals().items():
        if var_name.endswith('_pos') and isinstance(value, dict):
            element_name = var_name[:-4]
            # 确保对应的图片路径变量存在
            if element_name in globals():
                elements[element_name] = (globals()[element_name], value)
    return elements

class Config:
    """全局配置类"""
    # 基础置信度配置 - 降低默认置信度以适应实际情况
    DEFAULT_CONFIDENCE = 0.7  # 默认置信度
    HIGH_CONFIDENCE = 0.75    # 高置信度要求

    @classmethod
    def get_confidence_dict(cls) -> Dict[str, float]:
        """自动从brownDust2Dict中获取所有图像元素并设置置信度"""
        confidence_dict = {}
        for element_name, _ in get_scene_elements().items():
            # 根据元素类型设置不同的置信度
            if any(key in element_name.lower() for key in ['chat', 'skip', 'confirm']):
                confidence_dict[element_name] = cls.HIGH_CONFIDENCE
            else:
                confidence_dict[element_name] = cls.DEFAULT_CONFIDENCE
        return confidence_dict

    @classmethod
    def get_scene_patterns(cls) -> Dict[str, Dict]:
        """自动生成场景匹配模式"""
        patterns = {}
        confidence_dict = cls.get_confidence_dict()
        
        # 场景模式定义
        scene_patterns = {
            'mainline': ['mainline'],
            'interaction': ['mainline', 'inter'],
            'dialogue': ['skip'],
            'deep_dialogue': ['skipChat'],
            'battle': ['war'],
            'battle_end': ['exit'],
            'confirm': ['confirm'],
            'automove': ['autoMove'],
            'pause': ['pause'],
            'automainline': ['automainline'],
            'automainline_over': ['automainline_over'],
            'automainline_war': ['automainline_war']
        }
        
        # 生成场景模式
        for scene_name, required_elements in scene_patterns.items():
            patterns[scene_name] = {
                'confidence': {e: confidence_dict.get(e, cls.DEFAULT_CONFIDENCE) 
                             for e in required_elements if e in confidence_dict},
                'required': {e: True for e in required_elements}
            }
        
        return patterns

# 初始化配置
CONFIDENCE = Config.get_confidence_dict()
SCENE_MATCH = Config.get_scene_patterns()

class Scene(Enum):
    """游戏场景枚举，自动从处理函数生成"""
    UNKNOWN = auto()
    
    @classmethod
    def _generate_scenes(cls):
        """根据处理函数自动生成场景枚举"""
        scenes = {'UNKNOWN': cls.UNKNOWN}
        for name, func in globals().items():
            if name.startswith('handle_'):
                scene_name = name[7:].upper()
                scenes[scene_name] = auto()
        return scenes

# 场景处理函数
def handle_mainline(manager) -> None:
    """
    处理主线场景
    需要元素: mainline
    """
    click_random(mainLine_click)
    time.sleep(2)

def handle_interaction(manager) -> None:
    """
    处理交互场景
    需要元素: mainline, inter
    """
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

def handle_automainline(manager) -> None:
    """处理快速主线场景"""
    from utils import click_random  # 避免循环导入
    click_random(automainline_click)  # 随机点击automainline区域
    time.sleep(2)

def handle_automainline_over(manager) -> None:
    """处理快速主线完成场景"""
    from utils import click_random  # 避免循环导入
    click_random(automainline_click)  # 随机点击automainline区域
    time.sleep(2)

def handle_automainline_war(manager) -> None:
    """处理快速主线战斗场景"""
    from utils import click_random  # 避免循环导入
    click_random(automainline_click)  # 随机点击automainline区域
    time.sleep(2)

def get_scene_names():
    """获取所有场景名称"""
    scenes = ['UNKNOWN']  # 始终包含UNKNOWN场景
    for name in globals():
        if name.startswith('handle_'):
            scene_name = name[7:].upper()
            scenes.append(scene_name)
    return scenes

# 动态生成Scene枚举
Scene = Enum('Scene', {name: i for i, name in enumerate(get_scene_names())})

@dataclass
class ScenePattern:
    """场景特征模式"""
    elements: Dict[str, float]
    required_matches: Dict[str, bool]

@dataclass
class SceneConfig:
    """场景配置"""
    pattern: ScenePattern
    handler: Callable
    description: str

# 自动生成场景配置
def generate_scene_configs():
    """根据处理函数自动生成场景配置"""
    configs = {}
    for scene in Scene:
        if scene == Scene.UNKNOWN:
            continue
            
        handler_name = f"handle_{scene.name.lower()}"
        handler = globals().get(handler_name)
        
        if handler:
            scene_name = scene.name.lower()
            if scene_name in SCENE_MATCH:
                pattern = SCENE_MATCH[scene_name]
                
                # 安全地获取函数描述
                description = scene_name
                if handler.__doc__:
                    doc_lines = handler.__doc__.strip().split('\n')
                    if len(doc_lines) > 1:
                        description = doc_lines[1].strip()
                    else:
                        description = doc_lines[0].strip()
                
                configs[scene] = SceneConfig(
                    pattern=ScenePattern(
                        elements=pattern['confidence'],
                        required_matches=pattern['required']
                    ),
                    handler=handler,
                    description=description
                )
    return configs

SCENE_CONFIGS = generate_scene_configs()

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
                logging.error(f"模板文件不存在或无法读取: {target}")
                return None
            
            # 确保图像和模板大小合适
            if img.shape[0] < template.shape[0] or img.shape[1] < template.shape[1]:
                logging.warning(f"ROI区域({img.shape})小于模板大小({template.shape})")
                return None
            
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
                CONFIDENCE[element_name],  # 使用全局配置的置信度
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