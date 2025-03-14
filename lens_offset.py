import sys
import numpy as np
import os
import cv2
from logger import logger
import math


class LensOffset:
    """This class is used to fin the lens offset value from the given input image"""
    def __init__(self):
        """This function initializes dummy variables"""
        try:
            self.points = None
            self.image = None
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at init function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def validate_lens_offset(self, image, roi_width):
        try:
            """This function is used to find the center of the SFR reg to find the lens offset
            Inputs: 1. image - Input image
                    2. roi_width - Maximum radius for chart center placement
            Outputs: 1. self.image - Output image
                     2. dx - Deviation in x axis
                     3. dy - Deviation in y axis"""

            self.points = []
            self.image = image.copy()

            """Convert image to grayscale"""
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            gaussian = cv2.GaussianBlur(gray, (5, 5), 0)
            imagemean = np.mean(self.image)
            height, width, c = self.image.shape

            """Dynamic values for drawing in image"""
            if 500 < width < 1000:
                line_thickness = 2
                text_size = 1
                text_thickness = 1
            elif 1000 < width <= 1920:
                line_thickness = 2
                text_size = 1
                text_thickness = 2
            elif 1920 < width < 2592:
                line_thickness = 2
                text_size = 1
                text_thickness = 2
            elif 2592 <= width <= 3500:
                line_thickness = 2
                text_size = 1.5
                text_thickness = 2
            elif 3500 <= width < 4000:
                line_thickness = 3
                text_size = 2
                text_thickness = 2
            else:
                line_thickness = 3
                text_size = 2
                text_thickness = 2

            image_center = [int(width / 2), int(height / 2)]
            half_height = int(height / 2)
            half_width = int(width / 2)
            if imagemean > 50:
                ret, threshold = cv2.threshold(gaussian, 90, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            else:
                ret, threshold = cv2.threshold(gaussian, 90, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            kernel = np.ones((3, 3), np.uint8)
            threshold = cv2.erode(threshold, kernel, iterations=4)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            check_contour_count = 0
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:
                    check_contour_count += 1
            if check_contour_count:
                for contour in contours:

                    M = cv2.moments(contour)
                    if M['m00'] != 0:
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        area = cv2.contourArea(contour)
                        if cx - roi_width < image_center[0] < cx + roi_width and area > 500:
                            # if cy - 300 < image_center[1] < cy + 300:
                            if cy - roi_width < image_center[1] < cy + roi_width:
                                approximate = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
                                approximate = [item for sublist in approximate for item in sublist]
                                for i in approximate:
                                    self.points.append(i)
                req_point_1 = None
                req_point_2 = None
                temp = None
                for point1 in range(len(self.points) - 1):
                    for point2 in range(point1 + 1, len(self.points)):
                        distance = math.dist(self.points[point1], self.points[point2])
                        if point2 == 1:
                            temp = distance
                            req_point_1 = self.points[point1]
                            req_point_2 = self.points[point2]
                        else:
                            if distance < temp:
                                temp = distance
                                req_point_1 = self.points[point1]
                                req_point_2 = self.points[point2]

                offset_x1 = req_point_1[0]
                offset_y1 = req_point_1[1]
                offset_x2 = req_point_2[0]
                offset_y2 = req_point_2[1]
                mid_point = [int((offset_x2 + offset_x1) / 2), int((offset_y2 + offset_y1) / 2)]
                offset_x = mid_point[0]
                offset_y = mid_point[1]

                dx = offset_x - image_center[0]
                dy = offset_y - image_center[1]

                cv2.arrowedLine(self.image, (offset_x, offset_y), (offset_x, 0), (0, 0, 255), line_thickness,
                                tipLength=0.05)
                cv2.arrowedLine(self.image, (offset_x, offset_y), (offset_x, height), (0, 0, 255), line_thickness,
                                tipLength=0.05)
                cv2.arrowedLine(self.image, (offset_x, offset_y), (0, offset_y), (0, 0, 255), line_thickness,
                                tipLength=0.05)
                cv2.arrowedLine(self.image, (offset_x, offset_y), (width, offset_y), (0, 0, 255), line_thickness,
                                tipLength=0.05)
                cv2.putText(self.image, 'Image center position: {}'.format(image_center), (10, 55),
                            cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 0, 255), text_thickness, cv2.LINE_AA)
                cv2.putText(self.image, 'Lens center position: {}'.format(mid_point), (10, 130),
                            cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 0, 255), text_thickness, cv2.LINE_AA)
                cv2.putText(self.image, 'dx: {}px and dy: {}px'.format(dx, dy), (10, 205),
                            cv2.FONT_HERSHEY_SIMPLEX, text_size, (0, 0, 255), text_thickness, cv2.LINE_AA)

                cv2.arrowedLine(self.image, (half_width, half_height), (0, half_height), (0, 255, 0), line_thickness,
                                tipLength=0.05)
                cv2.arrowedLine(self.image, (half_width, half_height), (width, half_height), (0, 255, 0),
                                line_thickness,
                                tipLength=0.05)
                cv2.arrowedLine(self.image, (half_width, half_height), (half_width, 0), (0, 255, 0), line_thickness,
                                tipLength=0.05)
                cv2.arrowedLine(self.image, (half_width, half_height), (half_width, height), (0, 255, 0),
                                line_thickness,
                                tipLength=0.05)
                return self.image, dx, dy

            else:
                return self.image, "NA", "NA"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at validate_lens_offset function : {}|{}|{}|{}".format(exc_type, fname,
                                                                                       exc_tb.tb_lineno, e))
            return self.image, "NA", "NA"
