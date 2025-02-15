"""
布朗尘埃2自动化脚本
功能：
1. 自动完成主线任务
2. 支持场景识别和自动处理
3. 支持人工介入和脚本暂停

作者：liang
版本：2.0
"""

import time
import logging
import threading
import keyboard
from scene_config import Scene, SceneManager
from utils import setup_keyboard_control

# 日志配置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

def main():
    """主程序入口"""
    logging.info("====== 脚本初始化 ======")
    
    manager = SceneManager()
    setup_keyboard_control(manager)
    
    # 监听Esc键退出
    threading.Thread(
        target=lambda: keyboard.wait('esc'), 
        daemon=True
    ).start()
    
    logging.info("初始化完成，按Home键开始运行，End键暂停，Esc键退出")
    
    try:
        while True:
            if not manager.script_running or manager.manual_intervention_needed:
                time.sleep(0.5)
                continue
                
            try:
                cycle_start = time.time()
                
                current_scene = manager.identify_scene()
                if current_scene != Scene.UNKNOWN:
                    manager.handle_scene(current_scene)
                
                # 控制循环间隔
                elapsed = time.time() - cycle_start
                if elapsed < 0.5:  # 使用固定的0.5秒间隔
                    time.sleep(0.5 - elapsed)
                    
            except Exception as e:
                logging.error(f"循环处理异常: {e}")
                time.sleep(1)
                
    except KeyboardInterrupt:
        logging.info("用户终止脚本")
    finally:
        logging.info("====== 脚本结束 ======")

if __name__ == "__main__":
    main()