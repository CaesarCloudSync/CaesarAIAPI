import cv2
import numpy as np

import time



class CaesarYolo:
    def __init__(self) -> None:
        self.CONFIDENCE = 0.5
        self.SCORE_THRESHOLD = 0.5
        self.IOU_THRESHOLD = 0.5
        config_path = "CaesarObjectDetection/cfg/yolov3.cfg"
        weights_path = "CaesarObjectDetection/weights/yolov3.weights"
        self.font_scale = 1
        self.thickness = 1
        self.LABELS = open("CaesarObjectDetection/data/coco.names").read().strip().split("\n")
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3), dtype="uint8")

        self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

        self.ln = self.net.getLayerNames()
        try:
            self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        except IndexError:
            # in case getUnconnectedOutLayers() returns 1D array when CUDA isn't available
            self.ln = [self.ln[i - 1] for i in self.net.getUnconnectedOutLayers()]
        pass
    def caesar_object_detect(self,image):
        h, w = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.perf_counter()
        layer_outputs = self.net.forward(self.ln)
        time_took = time.perf_counter() - start
        print("Time took:", time_took)
        boxes, confidences, class_ids = [], [], []

        # loop over each of the layer outputs
        for output in layer_outputs:
            # loop over each of the object detections
            for detection in output:
                # extract the class id (label) and confidence (as a probability) of
                # the current object detection
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                # discard weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.CONFIDENCE:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # perform the non maximum suppression given the scores defined before
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.SCORE_THRESHOLD, self.IOU_THRESHOLD)

        self.font_scale = 1
        self.thickness = 1

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                x, y = boxes[i][0], boxes[i][1]
                w, h = boxes[i][2], boxes[i][3]
                # draw a bounding box rectangle and label on the image

                color = [int(c) for c in self.COLORS[class_ids[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color=color, thickness=self.thickness)
                text = f"{self.LABELS[class_ids[i]]}: {confidences[i]:.2f}"
                # calculate text width & height to draw the transparent boxes as background of the text
                (text_width, text_height) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=self.font_scale, thickness=self.thickness)[0]
                text_offset_x = x
                text_offset_y = y - 5
                box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height))
                overlay = image.copy()
                cv2.rectangle(overlay, box_coords[0], box_coords[1], color=color, thickness=cv2.FILLED)
                # add opacity (transparency to the box)
                image = cv2.addWeighted(overlay, 0.6, image, 0.4, 0)
                # now put the text (label: confidence %)
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=self.font_scale, color=(0, 0, 0), thickness=self.thickness)
        return image
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    caesaryolo = CaesarYolo()
    while True:
        _, image = cap.read()
        image = caesaryolo.caesar_object_detect(image)

        cv2.imshow("image", image)
        if ord("q") == cv2.waitKey(1):
            break

    cap.release()
    cv2.destroyAllWindows()
