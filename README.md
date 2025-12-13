# 🚀 Form Correctness Detection Using Pose Estimation

This project implements a complete **exercise form correctness detection system** using **MediaPipe Pose Estimation** and **rule-based geometric analysis**.  
It detects body keypoints from video, computes joint angles and alignment, and produces:

- 🎥 **Annotated exercise videos** with real-time feedback  
- 📊 **Frame-wise CSV metrics** for detailed quantitative analysis  

This project was developed as part of the **Smartan.AI Computer Vision Internship Task**.

---

## 🎥 Demo Videos

- **Explantion Video Pitch**
  https://drive.google.com/file/d/1sx_qQK093Vd7u7DH1GVarRlfffR1mv66/view?usp=sharing
  
- **Bicep Curl (Annotated)**  
  This Video present in out folder

- **Lateral Raise (Annotated)**  
  This Video present in out folder

- **Squat (Annotated)**  
  This Video present in out folder


## ⚠️ Environment & Execution Note (Important)

This project was executed in **Google Colab** because:

- ❌ Local Python environments had **version conflicts** with MediaPipe  
- ❌ MediaPipe redistributable binaries were **not compatible** with the local OS and Python version  
- ✅ Google Colab provides a **stable MediaPipe setup**, consistent Python versions, and smooth execution  

Therefore, all command examples in this repository use **Colab-style syntax** (`!python`, `%cd`, etc.).  
The codebase itself remains compatible with standard Python environments.

---

## 🚀 Key Features

- ✔ Human pose estimation using **MediaPipe Pose**
- ✔ Joint angle computation (elbow, shoulder, knee, back tilt)
- ✔ Symmetry and wrist–shoulder alignment checks
- ✔ Rule-based exercise correctness evaluation
- ✔ Real-time skeleton overlay and visual feedback
- ✔ Frame-wise CSV metrics generation
- ✔ Modular and extensible code architecture
- ✔ 📊 **MLflow experiment tracking support (Bonus)**

---

## 📁 Project Structure

```
Form-Correctness-Detection-Using-Pose-Estimation/
│── src/
│    ├── pose_detector.py        # MediaPipe pose extraction
│    ├── form_rules.py           # Angle calculations & rule logic
│    ├── smoothing.py            # Noise reduction utilities
│    ├── run_video.py            # End-to-end pipeline
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
│    ├── videos/
│    └── csv/
│
│── requirements.txt
│── README.md
│── REPORT.pdf
```

---

## 🛠 Installation

Install dependencies using:

```bash
pip install -r requirements.txt
```

### 📦 Main Dependencies
- mediapipe  
- opencv-python-headless  
- numpy  
- pandas  
- scipy  
- tqdm  
- mlflow (optional)

---

## ▶️ How to Run (Google Colab)

Navigate to the project directory:

```bash
%cd /content/Form-Correctness-Detection-Using-Pose-Estimation
```

---

### 🎯 Bicep Curl Analysis

```bash
!python -m src.run_video \
  --input "sample_videos/Bicep Curl.mp4" \
  --output "out/annotated_bicep.mp4" \
  --csv "out/metrics_bicep.csv"
```

---

### 🎯 Lateral Raise Analysis

```bash
!python -m src.run_video \
  --input "sample_videos/Lateral raise.mp4" \
  --output "out/annotated_lateral.mp4" \
  --csv "out/metrics_lateral.csv"
```

---

### 🎯 Squat Analysis

```bash
!python -m src.run_video \
  --input "sample_videos/Squat.mp4" \
  --output "out/annotated_squat.mp4" \
  --csv "out/metrics_squat.csv"
```

---

## 📊 MLflow Experiment Tracking (Bonus)

MLflow integration is included as an **optional enhancement** to track experiments, metrics, and outputs.

### 🚀 Run Squat Analysis with MLflow Enabled

```bash
!python -m src.run_video \
  --input "sample_videos/Squat.mp4" \
  --output "out/annotated_squat_mlflow.mp4" \
  --csv "out/metrics_squat_mlflow.csv" \
  --mlflow \
  --mlflow-experiment "Form-Correctness-Detection"
```

### 📈 What MLflow Logs
- 🔹 Input parameters (video name, FPS, frame count)
- 🔹 Statistical metrics (mean, min, max angles)
- 🔹 Artifacts (CSV files, annotated sample frames)

MLflow uses a **local SQLite backend**, which is suitable for Google Colab execution.

---

## 📊 Outputs

### 🎥 Annotated Videos

All annotated videos are stored in:

```
out/annotated_*.mp4
```

Each video includes:
- Pose skeleton overlay  
- Live joint angle visualization  
- Rule-based correctness feedback (`OK / BAD`)  

---

### 📈 CSV Metrics

Each exercise generates a CSV file containing frame-wise metrics such as:
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

## 🧠 Posture Rules Implemented

### 💪 Bicep Curl
- Elbow angle remains within a valid range  
- Shoulder remains stable  
- Wrist stays aligned with the elbow  

### 🏋️ Lateral Raise
- Wrist–Elbow–Shoulder alignment maintained  
- Symmetric arm raise  
- Avoid shoulder shrugging  

### 🦵 Squat
- Knee angle reaches sufficient depth  
- Back tilt remains within safe limits  
- Knees track over toes  

Detailed rule logic and thresholds are documented in **REPORT.pdf**.

---

## 📘 Project Report

The file `REPORT.pdf` contains:
- System pipeline explanation
- Mathematical derivation of joint angles
- Rule design and thresholds
- Noise handling strategies
- Multi-person handling approach
- Challenges faced and future scope

---

## 🚀 Future Improvements

- Automatic repetition counting  
- ML-based exercise quality scoring  
- Kalman filtering for smoother keypoints  
- Support for additional exercises  
- Web or mobile deployment  

---

## 👤 Author

**Yogesh Kharb**  
Computer Vision Internship Candidate  
GitHub: https://github.com/Yogeshkharb111

---

⭐ If you find this project useful, feel free to star the repository!
