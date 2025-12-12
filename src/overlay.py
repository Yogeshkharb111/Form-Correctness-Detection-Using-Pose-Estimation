"""Overlay drawing helpers for annotated output video."""
import cv2
import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose


def draw_landmarks(frame, landmarks):
    # landmarks: np.ndarray (33,3) normalized
    h, w = frame.shape[:2]
    for i, lm in enumerate(landmarks):
        x, y, v = lm
        cx, cy = int(x * w), int(y * h)
        if v > 0.1:
            cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)


def put_text_lines(frame, lines, org=(10, 20), color=(0, 255, 255)):
    x, y = org
    for i, line in enumerate(lines):
        cv2.putText(frame, line, (x, y + i * 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)


def annotate_frame(frame, landmarks, eval_dict):
    draw_landmarks(frame, landmarks)
    lines = []
    # build summary lines
    if 'bicep_curl' in eval_dict:
        for side, info in eval_dict['bicep_curl'].items():
            ok = 'OK' if info['ok'] else 'BAD'
            lines.append(f"{side} elbow: {info['angle']:.1f}° {ok}")
    if 'lateral_raise' in eval_dict:
        for side, info in eval_dict['lateral_raise'].items():
            ok = 'OK' if info['ok'] else 'BAD'
            lines.append(f"{side} lat-raise: {info['elbow_angle']:.1f}° {ok}")
    if 'back_posture' in eval_dict:
        bp = eval_dict['back_posture']
        lines.append(f"Back tilt: {bp['angle_deg']:.1f}° {'OK' if bp['ok'] else 'BAD'}")
    if 'squat' in eval_dict:
        sq = eval_dict['squat']
        if 'left' in sq:
            l = sq['left']
            lines.append(f"Squat L knee: {l['knee_angle']:.1f}° {'OK' if l['ok'] else 'BAD'}")
        if 'right' in sq:
            r = sq['right']
            lines.append(f"Squat R knee: {r['knee_angle']:.1f}° {'OK' if r['ok'] else 'BAD'}")
        lines.append(f"Torso tilt: {sq.get('torso_tilt', 0.0):.1f}° {'OK' if sq.get('ok', False) else 'BAD'}")
    put_text_lines(frame, lines, org=(10, 20))
    return frame
