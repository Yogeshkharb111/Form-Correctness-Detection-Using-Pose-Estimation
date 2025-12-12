"""Pose detection utilities using MediaPipe Pose.

Extracts 33 pose landmarks per frame and writes a CSV time-series
of keypoint x,y,visibility values.
"""
from dataclasses import dataclass
import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
from typing import Iterator, Tuple, Dict, Any

mp_pose = mp.solutions.pose


@dataclass
class FramePose:
    frame_index: int
    frame: np.ndarray
    landmarks: np.ndarray  # shape (33, 3) -> x, y, visibility


def extract_poses_from_video(video_path: str) -> Iterator[FramePose]:
    cap = cv2.VideoCapture(video_path)
    with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)
            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                arr = np.array([[l.x, l.y, l.visibility] for l in lm], dtype=float)
            else:
                arr = np.zeros((33, 3), dtype=float)
            yield FramePose(frame_index=idx, frame=frame, landmarks=arr)
            idx += 1
    cap.release()


def poses_to_dataframe(poses: Iterator[FramePose]) -> pd.DataFrame:
    rows = []
    for p in poses:
        flat = p.landmarks.flatten()
        d = {f"kp_{i}_{axis}": float(flat[i * 3 + axis_idx]) for i in range(33) for axis_idx, axis in enumerate(['x', 'y', 'v'])}
        d['frame'] = int(p.frame_index)
        rows.append(d)
    df = pd.DataFrame(rows)
    cols = ['frame'] + [c for c in df.columns if c != 'frame']
    return df[cols]


def save_pose_csv(video_path: str, out_csv: str) -> None:
    poses = extract_poses_from_video(video_path)
    df = poses_to_dataframe(poses)
    df.to_csv(out_csv, index=False)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    save_pose_csv(args.video, args.out)
