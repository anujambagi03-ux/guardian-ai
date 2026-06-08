from ultralytics import YOLO
import os


model = YOLO("yolov8n.pt")


def detect_vehicles(frames_folder="frames"):

    vehicle_classes = [
        "car",
        "motorcycle",
        "bus",
        "truck"
    ]

    vehicle_counts = {
        "car": 0,
        "motorcycle": 0,
        "bus": 0,
        "truck": 0
    }

    frame_files = os.listdir(frames_folder)

    for frame_file in frame_files:

        frame_path = os.path.join(
            frames_folder,
            frame_file
        )

        results = model(frame_path)

        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])

                class_name = model.names[class_id]

                if class_name in vehicle_classes:
                    vehicle_counts[class_name] += 1

    return vehicle_counts