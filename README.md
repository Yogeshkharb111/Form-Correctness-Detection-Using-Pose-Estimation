# Form Correctness Detection Using Pose Estimation

This project implements a complete **exercise form correctness detection system** using **MediaPipe Pose Estimation** and **rule-based geometric analysis**.  
It detects body keypoints from video, computes joint angles and alignment, and produces:

- Annotated exercise videos with real-time feedback  
- Frame-wise CSV metrics for detailed quantitative analysis  

This project was developed as part of the **Smartan.AI Computer Vision Internship Task**.

---

## Environment & Execution Note

This project was executed in **Google Colab** because:

- The local Python environment had version conflicts with MediaPipe.
- The required MediaPipe redistributable binaries were not compatible with the local OS and Python version.
- Google Colab provides a stable MediaPipe installation with consistent Python versions.

Therefore, all command examples in this repository use **Colab-style syntax** (`!python`, `%cd`, etc.).  
The code structure remains compatible with standard Python environments.

---

## Features

- Human pose estimation using MediaPipe Pose  
- Joint angle computation (elbow, shoulder, knee, back tilt)  
- Symmetry and wrist–shoulder alignment checks  
- Rule-based exercise correctness evaluation  
- Real-time skeleton overlay and visual feedback  
- Frame-wise CSV metrics generation  
- Modular and extensible code architecture  
- MLflow experiment logging support (optional)

---

## Project Structure

```
Form-Correctness-Detection-Using-Pose-Estimation/
│── src/
│    ├── pose_detector.py
│    ├── form_rules.py
│    ├── smoothing.py
│    ├── run_video.py
│
│── sample_videos/
│    ├── Bicep Curl.mp4
│    ├── Lateral raise.mp4
│    ├── Squat.mp4
│
│── out/
│    ├── annotated_bicep.mp4
│    ├── annotated_lateral.mp4
│    ├── annotated_squat.mp4
│    ├── metrics_bicep.csv
│    ├── metrics_lateral.csv
│    ├── metrics_squat.csv
│
│── mlflow_outputs/
│    ├── videos
│    └── csv
│
│── requirements.txt
│── README.md
│── REPORT.pdf
```

---

## Installation

Install dependencies using:

```bash
pip install -r requirements.txt
```

Main dependencies:
- mediapipe  
- opencv-python-headless  
- numpy  
- pandas  
- scipy  
- tqdm  
- mlflow 

---

## How to Run (Google Colab)

Navigate to the project directory:

```bash
%cd /content/Form-Correctness-Detection-Using-Pose-Estimation
```

### Bicep Curl

```bash
!python -m src.run_video \
  --input "sample_videos/Bicep Curl.mp4" \
  --output "out/annotated_bicep.mp4" \
  --csv "out/metrics_bicep.csv"
```

### Lateral Raise

```bash
!python -m src.run_video \
  --input "sample_videos/Lateral raise.mp4" \
  --output "out/annotated_lateral.mp4" \
  --csv "out/metrics_lateral.csv"
```

### Squat

```bash
!python -m src.run_video \
  --input "sample_videos/Squat.mp4" \
  --output "out/annotated_squat.mp4" \
  --csv "out/metrics_squat.csv"
```

---

## Outputs

### Annotated Videos

All annotated videos are stored in:

```
out/annotated_*.mp4
```

Each video includes:
- Pose skeleton overlay  
- Joint angle visualization  
- Rule-based correctness feedback  

---

### CSV Metrics

Each exercise produces a CSV file containing frame-wise metrics such as:
- Elbow angle  
- Shoulder alignment  
- Back tilt  
- Knee angle (squat)  
- Correctness flags  

Example:

```
frame, elbow_angle, back_tilt, is_correct
0, 45.6, 3.1, True
```

---

## Posture Rules Implemented

### Bicep Curl
- Elbow angle remains within a valid range  
- Shoulder remains stable  
- Wrist stays aligned with the elbow  

### Lateral Raise
- Wrist–Elbow–Shoulder alignment maintained  
- Symmetric arm raise  
- Avoid shoulder shrugging  

### Squat
- Knee angle reaches sufficient depth  
- Back tilt remains within safe limits  
- Knees track over toes  

Detailed rule logic is documented in **REPORT.pdf**.

---

## MLflow Integration (Optional)

MLflow is integrated to log:
- Experiment parameters
- Frame-wise metrics
- Output artifacts such as CSV files and sample frames

Tracking is done using a local SQLite backend, suitable for Google Colab environments.

---

## Project Report

The file `REPORT.pdf` contains:
- Pipeline overview
- Mathematical explanation of angle calculations
- Rule design and thresholds
- Noise handling techniques
- Multi-person handling strategy
- Challenges and future improvements

---

## Future Improvements

- Automatic repetition counting  
- ML-based exercise quality scoring  
- Kalman filtering for smoother keypoints  
- Support for additional exercises  
- Web or mobile deployment  

---

## Author

Yogesh Kharb  
Computer Vision Internship Candidate  
GitHub: https://github.com/Yogeshkharb111

---

If you find this project useful, feel free to star the repository.
