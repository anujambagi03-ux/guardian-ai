import cv2
import os


def extract_frames(video_path):
    """
    Extract frames from uploaded video
    """

    frames_folder = "frames"

    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)

    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    saved_frames = 0

    while True:
        success, frame = cap.read()

        if not success:
            break

        frame_count += 1

        # Save every 30th frame
        if frame_count % 30 == 0:
            frame_name = os.path.join(
                frames_folder,
                f"frame_{saved_frames}.jpg"
            )

            cv2.imwrite(frame_name, frame)
            saved_frames += 1

    cap.release()

    return {
        "total_frames_read": frame_count,
        "frames_saved": saved_frames,
        "frames_folder": frames_folder
    }