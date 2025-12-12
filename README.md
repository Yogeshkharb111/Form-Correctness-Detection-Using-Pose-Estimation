# Form Correctness Detection Using Pose Estimation

This project implements a complete **exercise form correctness detection system** using **MediaPipe Pose Estimation** and **rule-based geometric analysis**.  
It detects body keypoints from video, computes joint angles and alignment, and produces:

- **Annotated exercise videos** with real-time feedback  
- **Frame-wise CSV metrics** for detailed analysis  

This project was developed as part of the **Smartan.AI Computer Vision Internship Task**.

---

## 🚀 Features

- ✔ Human pose estimation using **MediaPipe**  
- ✔ Angle computation: elbow, shoulder, knee, back tilt  
- ✔ Symmetry and wrist-shoulder alignment checks  
- ✔ Rule-based correctness evaluation  
- ✔ Real-time drawing overlays on output video  
- ✔ CSV metrics for every frame  
- ✔ Clean, modular code architecture  
- ✔ MLflow integration ready (optional)

---

## 📁 Project Structure

```
smartan-form-checker/
│── src/
│    ├── pose_detector.py        # Handles MediaPipe pose extraction
│    ├── form_rules.py           # Angle rules and correctness logic
│    ├── smoothing.py            # Filters noisy pose keypoints
│    ├── run_video.py            # Full pipeline: detect → evaluate → annotate
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
│── requirements.txt
│── README.md
│── REPORT.pdf
```

---

## 🛠 Installation

Install all dependencies:

```bash
pip install -r requirements.txt
```

Required packages:

- mediapipe  
- opencv-python  
- numpy  
- pandas  

---

## ▶️ How to Run

Navigate to the project directory:

```bash
%cd /content/Project/smartan-form-checker
```

### 🎯 Run Bicep Curl Analysis

```bash
!python -m src.run_video \
    --input "sample_videos/Bicep Curl.mp4" \
    --output "out/annotated_bicep.mp4" \
    --csv "out/metrics_bicep.csv"
```

### 🎯 Run Lateral Raise Analysis

```bash
!python -m src.run_video \
    --input "sample_videos/Lateral raise.mp4" \
    --output "out/annotated_lateral.mp4" \
    --csv "out/metrics_lateral.csv"
```

### 🎯 Run Squat Analysis

```bash
!python -m src.run_video \
    --input "sample_videos/Squat.mp4" \
    --output "out/annotated_squat.mp4" \
    --csv "out/metrics_squat.csv"
```

---

## 📊 Outputs

### 🎥 Annotated Videos

Generated videos are stored here:

```
out/annotated_*.mp4
```

Each video includes:

- Pose skeleton overlay  
- Live joint angle calculations  
- Rule-based correctness messages  

---

### 📈 CSV Metrics

Each exercise produces a detailed CSV with:

- Elbow angle  
- Shoulder alignment values  
- Back tilt angle  
- Symmetry score  
- Knee angle (for squats)  
- Boolean correctness flags  

**Example row:**

```
frame, elbow_angle, shoulder_level, back_tilt, is_correct
0,     45.6,        0.12,           3.1,       True
```

---

## 🧠 Posture Rules Implemented

### Bicep Curl
- Elbow angle must decrease and increase smoothly  
- Shoulder should remain stable (minimal movement)  
- Wrist should stay aligned below or near the elbow  

### Lateral Raise
- Wrist → Elbow → Shoulder should form a straight horizontal line  
- Arms raise symmetrically on both sides  
- Shoulder elevation ("shrugging") must be avoided  

### Squat
- Knee angle should drop below threshold during descent  
- Back tilt angle must stay within a safe range  
- Knees should track above toes, not collapse inward  

More detailed logic is explained in **REPORT.pdf**.

---

## 📘 REPORT (PDF)

`REPORT.pdf` contains:

- Complete explanation of posture rules  
- Joint angle math and keypoint geometry  
- Noise reduction strategy (smoothing filters)  
- Handling multiple persons in a frame  
- Challenges and improvements  

---

## 🏗 Future Improvements

- Add ML-powered rep counting  
- Add exercise quality scoring model  
- Use Kalman filtering for smoother angles  
- Extend to more exercise types  
- Create a web/mobile live feedback application  

---

## 🤝 Author

**Yogesh Kharb**  
Smartan.AI Internship Candidate  
GitHub: https://github.com/Yogeshkharb111

---

## ⭐ If you find this project helpful, consider giving it a star!
