from ultralytics import YOLO
import cv2


model = YOLO("yolov8n.pt")


def detect_vehicles(image_path):

    results = model(image_path)

    detections = []

    image = cv2.imread(image_path)

    for result in results:

        boxes = result.boxes

        for box in boxes:

            cls = int(box.cls[0])

            label = model.names[cls]

            confidence = float(box.conf[0])

            if label in [
                "car",
                "bus",
                "truck",
                "motorcycle"
            ]:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                detections.append({
                    "vehicle_type": label,
                    "confidence": round(
                        confidence,
                        2
                    )
                })

                cv2.rectangle(
                    image,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    image,
                    f"{label} {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

    output_path = (
        "uploads/detected_result.jpg"
    )

    cv2.imwrite(
        output_path,
        image
    )

    return {
        "detections": detections,
        "output_image": output_path
    }