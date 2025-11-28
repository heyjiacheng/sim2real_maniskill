# 🤖 sim2real_maniskill

A ManiSkill-based project for capturing multi-view images and trajectory data for sim-to-real robotic manipulation.

### 📦 Installation

```bash
# Create conda environment
conda create -n mani python=3.12

# Install ManiSkill
pip install --upgrade mani_skill

# Activate environment
conda activate mani
```

## 📸 Usage

### 1️⃣ Capture Objects (`capture_custom_objects.py`)

Capture multi-view images of objects without robot interaction.

#### 🎯 Basic Examples

**Default object:**
```bash
python scripts/capture/capture_custom_objects.py
```

**Custom mesh object:**
```bash
python scripts/capture/capture_custom_objects.py --object-mesh-path dataset/customize/mug_obj/base.obj
```

**Articulated object (cabinet, drawer, etc.):**
```bash
python scripts/capture/capture_custom_objects.py --use-articulation --articulation-id 12536
```

**Custom position & rotation:**
```bash
python scripts/capture/capture_custom_objects.py --object-position 0 0 0.15 --object-rotation 90 0 0
```

#### ⚙️ Common Options

| Option | Description | Default |
|--------|-------------|---------|
| `--object-mesh-path` | Path to mesh file (.obj) | `dataset/customize/mug_obj/base.obj` |
| `--use-articulation` | Use articulated object | `False` |
| `--articulation-id` | Model ID for articulated objects | `12536` |
| `--object-position` | Position [x y z] in meters | `-0.05 0 0.15` |
| `--object-rotation` | Rotation [rx ry rz] in degrees | `0 0 10` |
| `--image-width` | Image width | `640` |
| `--image-height` | Image height | `480` |
| `--shader` | Renderer (`rt`, `rt-fast`, `default`) | `default` |

---

### 2️⃣ Capture Trajectory (`capture_trajectory.py`)

Execute robot trajectories and capture the entire manipulation process.

#### 🎯 Basic Examples

**Execute trajectory:**
```bash
python scripts/capture/capture_trajectory.py
```

**With articulated object:**
```bash
python scripts/capture/capture_trajectory.py --use-articulation --articulation-id 12536
```

**With grasp & lift:**
```bash
python scripts/capture/capture_trajectory.py --do-grasp-and-lift
```

**Custom robot & object positions:**
```bash
python scripts/capture/capture_trajectory.py \
    --robot-position 0.5 0 0 \
    --object-position -0.05 0 0.15 \
    --object-rotation 0 0 10
```

**Static capture (no trajectory):**
```bash
python scripts/capture/capture_trajectory.py --execute-trajectory False
```

#### ⚙️ Common Options

| Option | Description | Default |
|--------|-------------|---------|
| `--trajectory-path` | Path to trajectory JSON | `dataset/trajectory/.../trajectory.json` |
| `--execute-trajectory` | Execute the trajectory | `True` |
| `--show-trajectory-viz` | Show gripper visualizations | `True` |
| `--do-grasp-and-lift` | Grasp and lift after trajectory | `False` |
| `--ik-refine-steps` | IK refinement steps per point | `20` |
| `--robot-position` | Robot base position [x y z] | `None` |
| `--robot-rotation` | Robot base rotation [rx ry rz] | `0 0 0` |
| `--object-position` | Object position [x y z] | `-0.05 0 0.15` |
| `--object-rotation` | Object rotation [rx ry rz] | `0 0 10` |

## 📁 Output

Both scripts generate:

```
outputs/<timestamp>/
├── images/
│   ├── step_000000/
│   │   ├── front.png          # RGB image
│   │   ├── front_depth.npy    # Depth data
│   │   ├── front_depth.png    # Depth visualization
│   │   └── ... (other views)
│   └── ...
├── videos/
│   ├── front.mp4
│   ├── front_depth.mp4
│   └── ...
└── camera_params/
    ├── camera_params.json     # Camera parameters
    └── camera_params.npz
```

### 📷 Camera Views

6 predefined views: `front`, `behind`, `top`, `left`, `right`, `diagonal`

## 💡 Tips

- 📏 **Units**: Positions in meters, rotations in degrees
- 🎨 **Quality**: Use `--shader rt` for high-quality ray-traced rendering
- 🎬 **Video**: Videos are generated automatically if `--save-video True`
