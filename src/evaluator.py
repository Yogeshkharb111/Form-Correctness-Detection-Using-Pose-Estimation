"""Rule-based form evaluator.

Provides functions that compute angles and check three example rules:
- Bicep curl: elbow angle
- Lateral raise: wrist vs shoulder vertical alignment
- Back posture: torso lean angle

Each rule returns a dict with status and helpful message.
"""
from typing import Dict, Tuple
import numpy as np
import pandas as pd


def _angle_between(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
    """Angle at point b formed by a-b-c in degrees."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    v1 = a - b
    v2 = c - b
    denom = (np.linalg.norm(v1) * np.linalg.norm(v2))
    if denom == 0:
        return 0.0
    cosang = np.dot(v1, v2) / denom
    cosang = np.clip(cosang, -1.0, 1.0)
    ang = np.degrees(np.arccos(cosang))
    return float(ang)


def smooth_series(values: np.ndarray, window: int = 5) -> np.ndarray:
    if window <= 1:
        return values
    return np.convolve(values, np.ones(window) / window, mode='same')


def evaluate_bicep_curl(frame_landmarks: np.ndarray) -> Dict:
    """Check elbow angle (shoulder-elbow-wrist). Expects landmarks shape (33,3).

    Returns pass if elbow angle goes below ~40deg (curl) and above ~160deg (extended) at ends.
    For a single frame, we check if the elbow is within reasonable curl range (40-160) to give feedback.
    """
    # Left elbow (landmark 13) with shoulder 11 and wrist 15
    # Right elbow (14) with shoulder 12 and wrist 16
    results = {}
    for side in ['left', 'right']:
        if side == 'left':
            sh, el, wr = 11, 13, 15
        else:
            sh, el, wr = 12, 14, 16
        shoulder = tuple(frame_landmarks[sh, :2])
        elbow = tuple(frame_landmarks[el, :2])
        wrist = tuple(frame_landmarks[wr, :2])
        ang = _angle_between(shoulder, elbow, wrist)
        pass_ok = 30.0 <= ang <= 170.0
        msg = f"{side} elbow angle {ang:.1f}°"
        results[side] = {'angle': ang, 'ok': pass_ok, 'message': msg}
    return {'bicep_curl': results}


def evaluate_lateral_raise(frame_landmarks: np.ndarray) -> Dict:
    """For lateral raise, check wrist y coordinate relative to shoulder y (normalized image coords).

    If wrist y is close to shoulder y (within a tolerance) and arms are raised laterally (elbow angle near 180), then OK.
    """
    tol = 0.08  # tolerance in normalized coords
    results = {}
    for side in ['left', 'right']:
        if side == 'left':
            sh, el, wr = 11, 13, 15
        else:
            sh, el, wr = 12, 14, 16
        shoulder = frame_landmarks[sh, :2]
        elbow = frame_landmarks[el, :2]
        wrist = frame_landmarks[wr, :2]
        # since mediaPipe uses normalized y (0 top -> 1 bottom), closeness means small abs diff
        dy = abs(wrist[1] - shoulder[1])
        el_angle = _angle_between(shoulder, elbow, wrist)
        ok = dy <= tol and el_angle >= 150
        msg = f"{side} wrist-shoulder dy={dy:.3f}, elbow_ang={el_angle:.1f}°"
        results[side] = {'dy': float(dy), 'elbow_angle': el_angle, 'ok': bool(ok), 'message': msg}
    return {'lateral_raise': results}


def evaluate_back_posture(frame_landmarks: np.ndarray) -> Dict:
    """Estimate torso lean by angle between shoulders line and vertical, and hip-shoulder alignment.

    We compute vector from mid_hip to mid_shoulder and compare to vertical. Smaller deviation means upright back.
    """
    # shoulders: 11 (left), 12 (right); hips: 23 (left), 24 (right)
    left_sh = frame_landmarks[11, :2]
    right_sh = frame_landmarks[12, :2]
    left_hip = frame_landmarks[23, :2]
    right_hip = frame_landmarks[24, :2]
    mid_sh = (left_sh + right_sh) / 2.0
    mid_hip = (left_hip + right_hip) / 2.0
    vec = mid_sh - mid_hip
    # vertical vector pointing up (0, -1) in normalized coords
    vert = np.array([0.0, -1.0])
    denom = (np.linalg.norm(vec) * np.linalg.norm(vert))
    if denom == 0:
        ang = 0.0
    else:
        cosang = np.dot(vec, vert) / denom
        cosang = np.clip(cosang, -1.0, 1.0)
        ang = float(np.degrees(np.arccos(cosang)))
    ok = ang <= 12.0
    msg = f"torso tilt {ang:.1f}° (<=12° recommended)"
    return {'back_posture': {'angle_deg': ang, 'ok': bool(ok), 'message': msg}}


def evaluate_squat(frame_landmarks: np.ndarray) -> Dict:
    """Evaluate squat form using knee angle, torso tilt, and knee-over-ankle check.

    Landmarks used: hips 23/24, knees 25/26, ankles 27/28, shoulders 11/12.
    Returns per-side knee angles and basic pass/fail flags.
    """
    # indexes per MediaPipe pose
    L_HIP, R_HIP = 23, 24
    L_KNEE, R_KNEE = 25, 26
    L_ANKLE, R_ANKLE = 27, 28

    left_hip = frame_landmarks[L_HIP, :2]
    right_hip = frame_landmarks[R_HIP, :2]
    left_knee = frame_landmarks[L_KNEE, :2]
    right_knee = frame_landmarks[R_KNEE, :2]
    left_ankle = frame_landmarks[L_ANKLE, :2]
    right_ankle = frame_landmarks[R_ANKLE, :2]

    left_knee_ang = _angle_between(left_hip, left_knee, left_ankle)
    right_knee_ang = _angle_between(right_hip, right_knee, right_ankle)

    # torso tilt re-use of back_posture logic
    left_sh = frame_landmarks[11, :2]
    right_sh = frame_landmarks[12, :2]
    mid_sh = (left_sh + right_sh) / 2.0
    mid_hip = (left_hip + right_hip) / 2.0
    vec = mid_sh - mid_hip
    vert = np.array([0.0, -1.0])
    denom = (np.linalg.norm(vec) * np.linalg.norm(vert))
    if denom == 0:
        torso_angle = 0.0
    else:
        cosang = np.dot(vec, vert) / denom
        cosang = np.clip(cosang, -1.0, 1.0)
        torso_angle = float(np.degrees(np.arccos(cosang)))

    # knee-over-ankle check (side-view heuristic): how far forward knee is relative to ankle
    # uses normalized x difference (abs) — camera alignment matters
    left_knee_over = float(left_knee[0] - left_ankle[0])
    right_knee_over = float(right_knee[0] - right_ankle[0])

    # thresholds (tune per-camera):
    knee_depth_thresh = 100.0  # degrees or less indicates deeper squat
    torso_tilt_thresh = 25.0  # degrees
    knee_over_tolerance = 0.12  # normalized x units

    left_ok = left_knee_ang <= knee_depth_thresh and abs(left_knee_over) <= knee_over_tolerance and torso_angle <= torso_tilt_thresh
    right_ok = right_knee_ang <= knee_depth_thresh and abs(right_knee_over) <= knee_over_tolerance and torso_angle <= torso_tilt_thresh

    res = {
        'squat': {
            'left': {'knee_angle': left_knee_ang, 'knee_over': left_knee_over, 'ok': bool(left_ok),
                     'message': f"L knee {left_knee_ang:.1f}°, over {left_knee_over:.3f}"},
            'right': {'knee_angle': right_knee_ang, 'knee_over': right_knee_over, 'ok': bool(right_ok),
                      'message': f"R knee {right_knee_ang:.1f}°, over {right_knee_over:.3f}"},
            'torso_tilt': torso_angle,
            'ok': bool(left_ok and right_ok),
            'message': f"torso {torso_angle:.1f}° (<= {torso_tilt_thresh}°), depth L:{left_knee_ang:.1f} R:{right_knee_ang:.1f}"
        }
    }
    return res


def evaluate_frame(frame_landmarks: np.ndarray) -> Dict:
    # frame_landmarks expected shape (33,3)
    res = {}
    res.update(evaluate_bicep_curl(frame_landmarks))
    res.update(evaluate_lateral_raise(frame_landmarks))
    res.update(evaluate_back_posture(frame_landmarks))
    # squat evaluation
    try:
        res.update(evaluate_squat(frame_landmarks))
    except Exception:
        # be robust if landmarks missing
        res.update({'squat': {'error': 'could not evaluate squat'}})
    return res


if __name__ == '__main__':
    import numpy as np
    # small smoke test
    fake = np.zeros((33, 3), dtype=float)
    print(evaluate_frame(fake))