# 布朗尘埃2自动化脚本

一个用于自动化棕色尘埃2游戏主线任务的Python脚本工具集。

## 功能特点

- 自动完成主线任务
- 智能场景识别和处理
- 支持人工介入和脚本暂停
- 基于图像识别的自动化操作
- 可配置的识别参数
- 支持不同分辨率的屏幕

## 文件结构 
BrownDust2/
├── img/ # 图像模板目录
├── mainline.py # 主程序入口
├── scene_config.py # 场景配置和管理
├── utils.py # 工具函数
├── brownDust2Dict.py # 图像资源和位置信息
├── test.py # 窗口测试工具
└── README.md # 项目说明文档

## 主要组件

### 场景管理 (scene_config.py)
- 场景定义和识别
- 场景处理逻辑
- 全局配置管理
- 图像识别核心功能

### 工具函数 (utils.py)
- 安全点击操作
- 随机区域点击
- 键盘控制
- 对话框显示

### 图像资源 (brownDust2Dict.py)
- 图像模板路径
- 相对位置信息
- 点击区域定义

## 使用方法

1. 安装依赖：

```bash
pip install opencv-python mss numpy pyautogui pydirectinput keyboard
```

2. 配置图像模板：
   - 使用CaptureMarkHelper-PC.py工具截取所需图像
   - 图像会自动保存到img目录
   - 位置信息会自动更新到brownDust2Dict.py

3. 运行脚本：
```bash
python mainline.py
```

4. 控制命令：
   - Home键：开始运行/继续运行
   - End键：暂停脚本
   - Esc键：退出脚本

## 场景配置

可在scene_config.py中的Config类调整以下参数：

### 元素识别置信度
```python
CONFIDENCE = {
    'mainline': 0.7,    # 主线按钮
    'skip': 0.7,        # 跳过按钮
    'skipChat': 0.8,    # 对话跳过
    # ... 其他元素
}
```

### 场景匹配规则
```python
SCENE_MATCH = {
    'mainline': {
        'confidence': {'mainline': 0.7, 'inter': 0.85},
        'required': {'mainline': True, 'inter': False}
    },
    # ... 其他场景
}
```

## 注意事项

1. 运行前确保游戏窗口处于活动状态
2. 图像模板需要在相同分辨率下截取
3. 部分功能可能需要管理员权限
4. 建议在测试环境中先进行验证

## 开发说明

### 添加新场景

1. 在Scene枚举中添加新场景
2. 在Config.SCENE_MATCH中添加场景配置
3. 创建场景处理函数
4. 在SCENE_CONFIGS中注册场景配置

### 调试模式

可以通过调整日志级别来获取更详细的信息：
```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## 贡献

欢迎提交问题和改进建议。

## 许可证

MIT License
