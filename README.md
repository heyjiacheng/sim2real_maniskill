# 🤖 test_any_policy

A ManiSkill-based project for visualizing any robotic policy or trajectory.

### 📦 Installation

```bash
# Create conda environment
conda create -n mani python=3.12

# Activate environment
conda activate mani

# Install ManiSkill
pip install --upgrade mani_skill

# (Optional) Install Open3D
pip install open3d
```

## 📂 Data Preparation

### 🗄️ Articulated Objects

Download articulated objects (cabinets, drawers, etc.) from the PartNet-Mobility dataset:

1. **Browse & Download**: Visit [SAPIEN PartNet-Mobility Browser](https://sapien.ucsd.edu/browse)
2. **Extract**: Place downloaded models in `dataset/partnet_mobility/`
3. **Structure**: Each model should be in its own folder with the model ID as the folder name

```
dataset/
└── partnet_mobility/
    ├── 12536/          # Model ID
    │   ├── mobility.urdf
    │   └── ...
    ├── 45623/
    │   └── ...
    └── ...
```

### 🎨 Custom Mesh Objects

Place your custom 3D mesh files (.obj, .stl, etc.) in the `dataset/customize/` directory:

```
dataset/
└── customize/
    ├── mug_obj/
    │   └── base.obj
    ├── bottle_obj/
    │   └── model.obj
    └── your_object/
        └── mesh.obj
```

### 🛤️ Trajectory Files

Trajectory files (`trajectory.json`) contain the robot TCP (Tool Center Point) poses in **camera coordinate system**.

Convert to SAPIEN world coordinate here `src/trajectory_loader.py`

You can specify a custom trajectory with `--trajectory-path`.

## 📸 Usage

### GraspVLA Policy (`run_graspvla.py`)

Execute manipulation tasks using the GraspVLA vision-language-action policy.

> ⚠️ **Important**: Before running this script, you must launch the GraspVLA server separately:
> ```bash
> python others/GraspVLA/vla_network/scripts/serve.py \
>     --port 6666 \
>     --path <path_to_model>
> ```

#### 🎯 Basic Examples

**Default object with instruction:**
```bash
python scripts/graspvla/run_graspvla.py --instruction "pick up the mug"
```

---

### GraspVLA with PickClutterYCB (`run_graspvla_ycb.py`)

Execute manipulation tasks using GraspVLA policy with ManiSkill's PickClutterYCB-v1 environment (default YCB objects).

> ⚠️ **Important**: Before running, launch the GraspVLA server (same as above).

#### 🎯 Basic Examples

**Default scene:**
```bash
python scripts/graspvla/run_graspvla_ycb.py --instruction "pick up the object" --seed 42
```

### Capture Objects (`capture_custom_objects.py`)

Capture multi-view images of objects without robot interaction.

#### 🎯 Basic Examples

**Default object:**
```bash
python scripts/capture/capture_custom_objects.py
```

**Articulated object (cabinet, drawer, etc.):**
```bash
python scripts/capture/capture_custom_objects.py --use-articulation --articulation-id 12536
```

**Custom position & rotation:**
```bash
python scripts/capture/capture_custom_objects.py --object-position 0 0 0.15 --object-rotation 90 0 0
```

### Capture Trajectory (`capture_trajectory.py`)

Execute robot trajectories and capture the entire manipulation process.

#### 🎯 Basic Examples

**Generate Trajectory**
```bash
python scripts/capture/convert_gripper_pose.py 
```

**Custom robot & object positions:**
```bash
python scripts/capture/capture_trajectory.py --use_articulation --articulation_id 12536 --robot_position -0.6 -0.8 0 --robot_rotation 0 0 90
```

**Static capture (no trajectory):**
```bash
python scripts/capture/capture_trajectory.py --execute-trajectory False
```

**With grasp & lift:**
```bash
python scripts/capture/capture_trajectory.py --do-grasp-and-lift
```


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
