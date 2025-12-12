"""Run the full pipeline: pose detection -> evaluation -> annotate -> write video."""
import argparse
import os
import cv2
import numpy as np
from src.pose_detector import extract_poses_from_video
from src.evaluator import evaluate_frame
from src.overlay import annotate_frame
import pandas as pd
import tempfile
import warnings

try:
    import mlflow
    MLFLOW_AVAILABLE = True
except Exception:
    mlflow = None
    MLFLOW_AVAILABLE = False


def process_video(input_path: str, output_path: str, mlflow_log: bool = False, mlflow_experiment: str = None,
                  mlflow_tracking_uri: str = None, csv_out: str = None, display: bool = False):
    # prepare video capture info
    cap_tmp = cv2.VideoCapture(input_path)
    frame_count = int(cap_tmp.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    fps = cap_tmp.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cap_tmp.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap_tmp.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap_tmp.release()

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    if mlflow_log and not MLFLOW_AVAILABLE:
        warnings.warn("MLflow requested but not available (not installed). Continuing without MLflow.)")

    run = None
    if mlflow_log and MLFLOW_AVAILABLE:
        if mlflow_tracking_uri:
            mlflow.set_tracking_uri(mlflow_tracking_uri)
        if mlflow_experiment:
            mlflow.set_experiment(mlflow_experiment)
        run = mlflow.start_run()
        mlflow.log_param('input_video', os.path.basename(input_path))
        mlflow.log_param('frame_count', int(frame_count))
        mlflow.log_param('fps', float(fps))

    per_frame_rows = []

    sample_saved = False
    for frame_pose in extract_poses_from_video(input_path):
        frame_index = frame_pose.frame_index
        frame = frame_pose.frame
        lm = frame_pose.landmarks.copy()
        eval_res = evaluate_frame(lm)
        annotated = annotate_frame(frame, lm, eval_res)
        writer.write(annotated)

        # collect per-frame simple metrics
        bp = eval_res.get('back_posture', {}).get('angle_deg', None)
        left_elbow = eval_res.get('bicep_curl', {}).get('left', {}).get('angle', None)
        right_elbow = eval_res.get('bicep_curl', {}).get('right', {}).get('angle', None)
        per_frame_rows.append({'frame': int(frame_index), 'back_tilt': float(bp) if bp is not None else None,
                               'left_elbow': float(left_elbow) if left_elbow is not None else None,
                               'right_elbow': float(right_elbow) if right_elbow is not None else None})

        # log sample artifact (single frame) early so MLflow shows an example
        if mlflow_log and MLFLOW_AVAILABLE and not sample_saved and frame_index % max(1, int(fps)) == 0:
            tmpf = os.path.join(tempfile.gettempdir(), f"annotated_sample_{frame_index}.jpg")
            cv2.imwrite(tmpf, annotated)
            mlflow.log_artifact(tmpf, artifact_path='samples')
            sample_saved = True

    writer.release()

    # Save per-frame CSV if requested
    if csv_out:
        df = pd.DataFrame(per_frame_rows)
        df.to_csv(csv_out, index=False)
        if mlflow_log and MLFLOW_AVAILABLE:
            mlflow.log_artifact(csv_out, artifact_path='metrics')

    # summary MLflow metrics
    if mlflow_log and MLFLOW_AVAILABLE:
        df = pd.DataFrame(per_frame_rows)
        if not df.empty:
            for col in ['back_tilt', 'left_elbow', 'right_elbow']:
                if col in df.columns and df[col].dropna().size > 0:
                    mlflow.log_metric(f"{col}_mean", float(df[col].mean()))
                    mlflow.log_metric(f"{col}_min", float(df[col].min()))
                    mlflow.log_metric(f"{col}_max", float(df[col].max()))
        mlflow.end_run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--mlflow', action='store_true', help='Enable MLflow logging if available')
    parser.add_argument('--mlflow-experiment', type=str, default=None, help='MLflow experiment name')
    parser.add_argument('--mlflow-tracking-uri', type=str, default=None, help='MLflow tracking uri')
    parser.add_argument('--csv', type=str, default=None, help='Save per-frame metrics CSV')
    parser.add_argument('--display', action='store_true', help='Display annotated frames while processing')
    args = parser.parse_args()
    process_video(args.input, args.output, mlflow_log=args.mlflow, mlflow_experiment=args.mlflow_experiment,
                  mlflow_tracking_uri=args.mlflow_tracking_uri, csv_out=args.csv, display=args.display)


if __name__ == '__main__':
    main()
