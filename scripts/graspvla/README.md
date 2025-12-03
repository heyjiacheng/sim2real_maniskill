# GraspVLA + ManiSkill Integration

This directory integrates the GraspVLA Vision-Language-Action (VLA) model with the ManiSkill simulation environment, replacing the original LIBERO environment used in GraspVLA playground.

## System Architecture

```
┌──────────────────────────────────────────────────┐
│  GraspVLA Policy Server (ZMQ Port: 6666)         │
│  - Receives: images + proprioception history     │
│  - Outputs: delta actions (relative movements)   │
└────────────────┬─────────────────────────────────┘
                 │ ZMQ Communication
┌────────────────▼─────────────────────────────────┐
│  RemoteAgent (remote_agent.py)                   │
│  - Collects observations from ManiSkill          │
│  - Converts: world frame → robot base frame      │
│  - Converts: delta actions → absolute actions    │
│  - Converts: GraspVLA gripper ↔ ManiSkill        │
└────────────────┬─────────────────────────────────┘
                 │ Absolute poses
┌────────────────▼─────────────────────────────────┐
│  ManiSkill Environment                           │
│  - IK solver: pose → joint positions             │
│  - Physics simulation + rendering                │
└──────────────────────────────────────────────────┘
```

## Files

- **`remote_agent.py`**: Communicates with GraspVLA server, handles all data conversions
- **`run_graspvla.py`**: Run GraspVLA with custom objects
- **`run_graspvla_ycb.py`**: Run GraspVLA with standard PickClutterYCB-v1 environment

## Critical Design Decisions

### 1. Coordinate Frame: Robot Base Frame

**Why?** GraspVLA was trained with LIBERO using robot-relative coordinates.

**Implementation:**
- ManiSkill provides TCP pose in world frame
- **Must convert** to robot base frame: `tcp_base = base_world.inv() * tcp_world`
- All subsequent processing stays in robot base frame
- This ensures the model sees the same coordinate distribution as during training

### 2. Gripper Convention Conversion

**GraspVLA (trained with LIBERO):** -1 (close), 0 (no change), 1 (open)
**ManiSkill:** 0 (close), 1 (open)

**RemoteAgent handles conversion:**
- Uses internally tracked `finger_state` to avoid observation noise
- Inserts 4 identical actions during gripper transitions for smooth control

### 3. Delta to Absolute Actions

**GraspVLA outputs:** Relative movements (deltas)
**ManiSkill IK needs:** Absolute poses

**Conversion:**
- Position: `next_pos = current_pos + delta_pos`
- Rotation: `next_R = delta_R @ current_R` (matrix multiplication)
- Actions are accumulated in robot base frame

## Usage

### Step 1: Start the GraspVLA Policy Server

First, launch the GraspVLA policy server in a separate terminal:

```bash
cd others/GraspVLA/vla_network
python scripts/serve.py --port 6666 --path <path_to_your_model_checkpoint>
```

The server will:
- Load the VLA model
- Warm up with test samples
- Listen on port 6666 for ZMQ requests

### Step 2: Run the ManiSkill Integration

Once the server is running, launch the ManiSkill integration:

#### Basic Usage

```bash
# Run with default mug object
python scripts/graspvla/run_graspvla.py --instruction "pick up the mug"
```

#### Custom Object

```bash
# Use a custom mesh file
python scripts/graspvla/run_graspvla.py \
    --instruction "pick up the bottle" \
    --object-mesh-path dataset/customize/bottle/base.obj \
    --object-position -0.05 0 0.15
```

#### Articulated Object

```bash
# Use PartNet-Mobility articulated object
python scripts/graspvla/run_graspvla.py \
    --instruction "open the cabinet door" \
    --use-articulation \
    --articulation-id 12536 \
    --object-position -0.15 0 0
```

#### Custom Robot and Object Positions

```bash
python scripts/graspvla/run_graspvla.py \
    --instruction "pick up the mug" \
    --robot-position 0.5 0 0 \
    --robot-rotation 0 0 45 \
    --object-position -0.05 0 0.15 \
    --object-rotation 0 0 10
```

#### Debug Mode

```bash
# Enable debug output to see detailed information
python scripts/graspvla/run_graspvla.py \
    --instruction "pick up the mug" \
    --debug
```

### Step 3: View Results

After running, results are saved to `outputs/graspvla/<timestamp>/`:
- `images/`: Multi-view camera images for each timestep
- `camera_params/`: Camera intrinsic and extrinsic parameters
- `videos/`: Generated videos from different camera viewpoints (if `--save-video` is enabled)

## Key Arguments

**Required:**
- `--instruction`: Task instruction (e.g., "pick up the mug")

**Common:**
- `--port`: GraspVLA server port (default: 6666)
- `--object-mesh-path`: Path to custom object mesh
- `--object-position`: Object position [x, y, z]
- `--robot-position`: Robot base position [x, y, z]
- `--max-steps`: Max steps per episode (default: 300)
- `--debug`: Enable debug output

**For articulated objects:**
- `--use-articulation`: Enable articulation mode
- `--articulation-id`: Model ID (e.g., "12536")

See `--help` for full list of arguments.

## Data Flow

1. **ManiSkill** renders images, provides TCP pose (world frame) and gripper state
2. **RemoteAgent** converts to robot base frame, maintains 4-frame history
3. **GraspVLA Server** receives observation, returns delta actions (chunk of 8-16)
4. **RemoteAgent** accumulates deltas into absolute poses
5. **ManiSkill** solves IK and executes joint commands

## Troubleshooting

**"Failed to connect to policy server"**
- Ensure GraspVLA server is running: `python others/GraspVLA/vla_network/scripts/serve.py --port 6666 --path <model>`
- Check port matches between server and client

**"IK solution not found"**
- Target pose may be unreachable
- Try adjusting `--object-position` or `--robot-position`

**"No URDF file found"**
- Verify articulation dataset is downloaded in `dataset/<dataset_name>/<model_id>/`

## Dependencies

- ManiSkill, PyTorch, NumPy, transforms3d, ZMQ, CuRobo, tyro, scipy
