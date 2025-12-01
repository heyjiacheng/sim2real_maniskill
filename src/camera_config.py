"""
相机配置模块

定义常用的相机视角配置
"""

from typing import Dict, Tuple, List


# 相机视角配置（世界坐标系）
# 格式: {视角名称: (相机位置, 朝向目标点)}
# 这套配置用于 capture_trajectory.py 等常规脚本
CAMERA_VIEWS: Dict[str, Tuple[List[float], List[float]]] = {
    # 标准视角（世界坐标系）
    "front": ([1.3, 0.0, 1.2], [0.0, 0.0, 0.1]),
    "behind": ([-1.3, 0.0, 1.2], [0.0, 0.0, 0.1]),
    "top": ([0.0, 0.0, 1.8], [0.0, 0.0, 0.1]),
    "left": ([0.0, 1.3, 0.8], [0.0, 0.0, 0.1]),
    "right": ([0.0, -1.3, 0.8], [0.0, 0.0, 0.1]),
    "diagonal": ([1.0, 1.0, 1.2], [0.0, 0.0, 0.1]),
}


# GraspVLA 相机配置（机械臂坐标系）
# 这套配置用于 run_graspvla.py
# 注意：位置是相对于机械臂坐标系，在 setup_cameras 中会自动转换到世界坐标系
GRASPVLA_CAMERA_VIEWS: Dict[str, Tuple[List[float], List[float]]] = {
    "front": ([1.35, 0.0, 0.53], [0.2, 0.0, 0.0]),      # Front Camera
    "left": ([0.5, 0.69, 0.5], [0.5, 0.0, 0.1]),         # Side Camera
}


# 预定义的相机配置集合
CAMERA_VIEW_SETS = {
    "basic": ["front", "top"],
    "standard": ["front", "top", "left", "right"],
    "full": ["front", "top", "left", "right", "diagonal"],
}


def get_camera_views(preset: str = "full") -> Dict[str, Tuple[List[float], List[float]]]:
    """
    获取预设的相机视角配置

    Args:
        preset: 预设名称 ("basic", "standard", "full" 或自定义视角列表)

    Returns:
        相机视角配置字典
    """
    if preset == "all" or preset == "full":
        return CAMERA_VIEWS

    if preset in CAMERA_VIEW_SETS:
        view_names = CAMERA_VIEW_SETS[preset]
        return {name: CAMERA_VIEWS[name] for name in view_names if name in CAMERA_VIEWS}

    # 如果传入的是逗号分隔的视角名称
    if isinstance(preset, str) and "," in preset:
        view_names = [name.strip() for name in preset.split(",")]
        return {name: CAMERA_VIEWS[name] for name in view_names if name in CAMERA_VIEWS}

    return CAMERA_VIEWS


def list_available_views() -> List[str]:
    """列出所有可用的相机视角名称"""
    return list(CAMERA_VIEWS.keys())


def add_custom_view(
    name: str,
    position: List[float],
    look_at: List[float]
) -> None:
    """
    添加自定义相机视角

    Args:
        name: 视角名称
        position: 相机位置 [x, y, z]
        look_at: 朝向目标点 [x, y, z]
    """
    CAMERA_VIEWS[name] = (position, look_at)
