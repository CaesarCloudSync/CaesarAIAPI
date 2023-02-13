import cv2
import numpy as np



class CaesarFaceDetection:
    def __init__(self) -> None:
        # https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
        prototxt_path = "CaesarFaceDetection/weights/deploy.prototxt.txt"
        # https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel 
        model_path = "CaesarFaceDetection/weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"

        # load Caffe model
        self.model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    def detect_face(self,image, showtext=False,snapcropface=False):
        h, w = image.shape[:2]
        # preprocess the image: resize and performs mean subtraction
        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
        # set the image into the input of the neural network
        self.model.setInput(blob)
        # perform inference and get the result
        output = np.squeeze(self.model.forward())
        font_scale = 1.0
        for i in range(0, output.shape[0]):
            # get the confidence
            confidence = output[i, 2]
            # if confidence is above 50%, then draw the surrounding box
            if confidence > 0.5:
                # get the surrounding box cordinates and upscale them to original image
                box = output[i, 3:7] * np.array([w, h, w, h])
                # convert to integers
                start_x, start_y, end_x, end_y = box.astype(np.int)
                # draw the rectangle surrounding the face
                start_point = (start_x, start_y)
                end_point = (end_x, end_y)
                if snapcropface == True:
                    factor_add = 20
                    crop_img = image[start_y- factor_add:end_y+ factor_add, start_x- factor_add:end_x + factor_add]
                    return crop_img
                    #cv2.imshow("cropped", crop_img)
                    #cv2.waitKey(0)
                
                cv2.rectangle(image,start_point,end_point, color=(255, 0, 0), thickness=2)
                # draw text as well
                if showtext == True:
                    cv2.putText(image, f"{confidence*100:.2f}%", (start_x, start_y-5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 2)
        if snapcropface != True:
            return image
