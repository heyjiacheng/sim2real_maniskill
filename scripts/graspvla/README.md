# GraspVLA + ManiSkill Integration

This directory contains code to integrate the GraspVLA robot motion policy with the ManiSkill simulation environment.

## Overview

The integration replaces the LIBERO simulation environment used in the original GraspVLA playground with ManiSkill, allowing you to:
- Run GraspVLA policies in ManiSkill environments
- Load custom objects (regular meshes or articulated objects)
- Visualize and save multi-view camera observations
- Execute learned manipulation policies with IK control

## Architecture

```
┌─────────────────────────────────────────┐
│  GraspVLA Policy Server (ZMQ)           │
│  (others/GraspVLA/vla_network/          │
│   scripts/serve.py)                     │
└────────────────┬────────────────────────┘
                 │ ZMQ Communication
                 │ (observations → actions)
┌────────────────▼────────────────────────┐
│  RemoteAgent                            │
│  - Sends observations (images, proprio) │
│  - Receives delta actions               │
│  - Converts to absolute actions         │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  ManiSkill Environment                  │
│  - Renders camera images                │
│  - Executes actions via IK              │
│  - Simulates physics                    │
└─────────────────────────────────────────┘
```

## Files

- **`remote_agent.py`**: RemoteAgent class that communicates with GraspVLA policy server via ZMQ
- **`run_graspvla.py`**: Main script to run episodes with GraspVLA policy in ManiSkill
- **`README.md`**: This file

## Usage

### Step 1: Start the GraspVLA Policy Server

First, launch the GraspVLA policy server in a separate terminal:

```bash
cd others/GraspVLA/vla_network
python scripts/serve.py --port 5555 --path <path_to_your_model_checkpoint>
```

The server will:
- Load the VLA model
- Warm up with test samples
- Listen on port 5555 for ZMQ requests

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

## Command Line Arguments

### Environment Settings
- `--env-id`: ManiSkill environment ID (default: "PickCube-v1")
- `--sim-backend`: Simulation backend, "auto", "cpu", or "gpu" (default: "auto")
- `--render-backend`: Rendering backend, "cpu" or "gpu" (default: "gpu")
- `--shader`: Shader type, "rt", "rt-fast", or "default" (default: "rt")
- `--seed`: Random seed for reproducibility

### Policy Server Connection
- `--port`: ZMQ server port where GraspVLA is running (default: 5555)
- `--instruction`: Task instruction text (e.g., "pick up the mug")

### Object Loading

**Mode 1: Regular Mesh Object**
- `--object-mesh-path`: Path to object mesh file (default: "dataset/customize/mug_obj/base.obj")

**Mode 2: Articulated Object**
- `--use-articulation`: Enable articulation mode
- `--articulation-id`: Model ID from dataset (e.g., "12536")
- `--articulation-dataset`: Dataset name (default: "partnet-mobility")

**Common Object Settings**
- `--object-position`: Object position [x, y, z] in meters (default: -0.05 0 0.15)
- `--object-rotation`: Object rotation [rx, ry, rz] in degrees (default: 0 0 10)

### Robot Settings
- `--robot-position`: Robot base position [x, y, z] in meters (default: None = use default)
- `--robot-rotation`: Robot base rotation [rx, ry, rz] in degrees (default: 0 0 0)

### Camera and Rendering
- `--image-width`: Camera image width in pixels (default: 256, GraspVLA expects 256x256)
- `--image-height`: Camera image height in pixels (default: 256)
- `--hide-goal`: Hide goal markers in the scene (default: True)

### Episode Settings
- `--max-steps`: Maximum steps per episode (default: 300)
- `--save-video`: Save videos after episode (default: True)
- `--video-fps`: Video frame rate (default: 10)

### Output
- `--output-root`: Root directory for outputs (default: "outputs/graspvla")

### Debug
- `--debug`: Enable debug output with detailed information

## Key Differences from LIBERO

1. **Observation Format**:
   - LIBERO: Uses `robot0_joint_pos` for proprioception and specific image keys
   - ManiSkill: Extracts TCP pose directly from robot state, renders custom cameras

2. **Action Execution**:
   - LIBERO: Uses robot's built-in IK or joint control
   - ManiSkill: Uses CuRobo IK solver for accurate pose control

3. **Gripper Convention**:
   - GraspVLA: -1 (closed), 0 (no change), 1 (open)
   - ManiSkill: 0 (closed), 1 (open)
   - RemoteAgent handles the conversion automatically

4. **Camera Setup**:
   - LIBERO: Fixed camera positions based on scene
   - ManiSkill: Customizable cameras defined in `CAMERA_VIEWS`

## Troubleshooting

### "Failed to connect to policy server"
- Make sure the GraspVLA server is running on the specified port
- Check that the port number matches in both server and client
- Verify no firewall is blocking localhost connections

### "IK solution not found"
- The target pose may be unreachable for the robot
- Try adjusting object or robot positions
- Check if the workspace is within robot's reach

### "No URDF file found"
- Make sure the articulation dataset is properly downloaded
- Check the path format: `dataset/<dataset_name>/<model_id>/`
- Verify the model ID exists in the dataset

### Images are too dark/bright
- Adjust shader settings: try `--shader rt-fast` or `--shader default`
- Check camera positions and lighting in the scene

## Dependencies

- ManiSkill (with GPU simulation)
- PyTorch
- NumPy
- transforms3d
- ZMQ (pyzmq)
- CuRobo (for IK solving)
- tyro (for command line arguments)
- scipy (for rotation utilities)

## References

- Original GraspVLA playground: `others/GraspVLA/GraspVLA-playground/`
- GraspVLA policy server: `others/GraspVLA/vla_network/scripts/serve.py`
- ManiSkill trajectory capture: `scripts/capture/capture_trajectory.py`
