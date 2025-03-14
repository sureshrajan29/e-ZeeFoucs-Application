import os
import sys
import cv2
import numpy as np
import imutils
import math
from scipy import interpolate
import threading
from logger import logger


class MTFCalculation:
    """This class is used for MTF calculation"""
    roi_mtf_value = None
    image = None

    def __init__(self, alg=str, roi_list=None, all_channel=False):
        """The init function takes the following inputs:
        1. Type of preprocessing
        2. ROI Inputs
        3. Channel for MTF validation
        and splits the ROIs into two threads for validation"""

        self.roi_mtf_value = roi_list
        self.CN = alg

        if all_channel:
            self.channels = ['roi_lum', 'roi_red', 'roi_green', 'roi_blue']
        else:
            self.channels = ['roi_lum']
        thread_one = list(roi_list.keys())[:int(len(roi_list.keys()) / 2)]
        thread_two = list(roi_list.keys())[int(len(roi_list.keys()) / 2):]
        thread_1 = threading.Thread(target=self.run_thread, args=[thread_one])
        thread_1.start()
        thread_2 = threading.Thread(target=self.run_thread, args=[thread_two])
        thread_2.start()
        thread_1.join()
        thread_2.join()

    def run_thread(self, roi_positions):
        """This function loops through the regions in the ROI and validates calls the rotate_roi, esf_calculation
        lsf_calculation, mtf_calculation in sequence
        Inputs: roi_positions"""

        for roi_position in roi_positions:
            roi_regions = self.roi_mtf_value[roi_position]
            if roi_regions:
                for region in range(len(roi_regions)):
                    self.roi_mtf_value[roi_position][region]['roi_lum'] = {}
                    self.roi_mtf_value[roi_position][region]['roi_red'] = {}
                    self.roi_mtf_value[roi_position][region]['roi_green'] = {}
                    self.roi_mtf_value[roi_position][region]['roi_blue'] = {}
                    self.rotate_roi(roi_position, region)
                    self.esf_calculation(roi_position, region)
                    self.lsf_calculation(roi_position, region)
                    self.mtf_calculation(roi_position, region)
            else:
                logger.debug("There are no ROI in {} position".format(roi_position))

    def rotate_roi(self, roi_position, region):
        """This function finds the ROI edge angle and calculates the edge poly, which is used to traverse the pixels.
        Inputs: 1. roi_position
                2. region"""
        try:
            roi_img = self.roi_mtf_value[roi_position][region]['roi_img']
            for channel in self.channels:
                if channel == 'roi_lum':
                    if self.CN != "CN":
                        gray = (roi_img[:, :, 2] * 0.2126 + roi_img[:, :, 1] * 0.7152 + roi_img[:, :, 0] * 0.0722)
                    else:
                        gray = roi_img
                elif channel == 'roi_red':
                    gray = roi_img[:, :, 2]
                elif channel == 'roi_green':
                    gray = roi_img[:, :, 1]
                elif channel == 'roi_blue':
                    gray = roi_img[:, :, 0]

                tl = np.average(gray[0:2, 0:2])
                tr = np.average(gray[0:2, -3:-1])
                bl = np.average(gray[-3:-1, 0:2])
                br = np.average(gray[-3:-1, -3:-1])
                edges = [tl, tr, bl, br]
                edgeIndexes = np.argsort(edges)

                if (edgeIndexes[0] + edgeIndexes[1]) == 1:
                    pass
                elif (edgeIndexes[0] + edgeIndexes[1]) == 5:
                    gray = np.rot90(gray, 2)
                elif (edgeIndexes[0] + edgeIndexes[1]) == 2:
                    gray = np.rot90(gray, 3)
                elif (edgeIndexes[0] + edgeIndexes[1]) == 4:
                    gray = np.rot90(gray)

                roi_blur = cv2.GaussianBlur(np.uint8(gray), (5, 5), 0)  # Added to get proper edge
                ret, roi_thresh = cv2.threshold(roi_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                rio_canny = cv2.Canny(roi_thresh, 40, 90, L2gradient=True)
                line = np.argwhere(rio_canny == 255)
                edge_poly = np.polyfit(line[:, 1], line[:, 0], 1)
                # print(edge_poly, "edge_poly")
                slant_angle = math.degrees(math.atan(-edge_poly[0]))

                final_edge_poly = edge_poly.copy()
                if slant_angle > 0:
                    gray = np.flip(gray, axis=1)
                    final_edge_poly[1] = np.polyval(edge_poly, np.size(roi_img, 1) - 1)
                    final_edge_poly[0] = -edge_poly[0]

                self.roi_mtf_value[roi_position][region][channel]['img'] = gray
                self.roi_mtf_value[roi_position][region][channel]['edge_poly'] = final_edge_poly
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at rotate_roi function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def esf_calculation(self, roi_position, region):
        """This function computes the head and tail, which is used to set min and max for ESF calculation, there are two
        conditions to calculate the ESF
        1. Static ESF: -10 to 10.
        2. Dynamic ESF: 5 to 95 percent of the available ESF(This can be used when the ROI is small and we are unable to
         extract -10 to 10 data).
        Inputs: 1. roi_position
                2. region"""
        try:
            for channel in self.channels:
                gray = self.roi_mtf_value[roi_position][region][channel]['img']
                edge_poly = self.roi_mtf_value[roi_position][region][channel]['edge_poly']

                height = gray.shape[0]
                width = gray.shape[1]
                values = np.reshape(gray, width * height)
                distance = np.zeros((height, width))
                column = np.arange(0, width) + 0.5

                for y in range(height):
                    distance[y, :] = (edge_poly[0] * column - (y + 0.5) + edge_poly[1]) / np.sqrt(
                        edge_poly[0] * edge_poly[0] + 1)

                distances = np.reshape(distance, width * height)
                indexes = np.argsort(distances)
                sign = 1
                if np.average(values[indexes[:10]]) > np.average(values[indexes[-10:]]):
                    sign = -1
                values = values[indexes]
                distances = sign * distances[indexes]
                if distances[0] > distances[-1]:
                    distances = np.flip(distances)
                    values = np.flip(values)
                maximum = np.amax(values)
                minimum = np.amin(values)
                threshold = (maximum - minimum) * 0.1
                head = np.amax(distances[(np.where(values < minimum + threshold))[0]])
                tail = np.amin(distances[(np.where(values > maximum - threshold))[0]])
                width = abs(head - tail)
                if width < 1:
                    head = head - 0.2
                    tail = tail + 0.2
                else:
                    head = head - 1.2 * width
                    tail = tail + 1.2 * width

                is_incrementing = True
                if distances[0] > distances[-1]:
                    is_incrementing = False
                    distances = -distances
                    dummy = -tail
                    tail = -head
                    head = dummy

                hindex = (np.where(distances < head)[0])
                tindex = (np.where(distances > tail)[0])
                if hindex.size < 2:
                    h = 0
                else:
                    h = np.amax(hindex)

                if tindex.size == 0:
                    t = distances.size
                else:
                    t = np.amin(tindex)

                if is_incrementing is False:
                    distances = -distances

                """-10 to 10"""
                h = np.amax(np.where(distances < -10))
                t = np.amin(np.where(distances > 10))
                """-10 to 10 """

                self.roi_mtf_value[roi_position][region][channel]['distances'] = distances
                self.roi_mtf_value[roi_position][region][channel]['values'] = values
                self.roi_mtf_value[roi_position][region][channel]['esf_distances'] = distances[h:t]
                self.roi_mtf_value[roi_position][region][channel]['esf_values'] = values[h:t]
                self.roi_mtf_value[roi_position][region][channel]['10_90_rise'] = width


                qs = np.linspace(0, 1, 20)[1:-1]
                knots = np.quantile(distances[h:t], qs)
                tck = interpolate.splrep(distances[h:t], values[h:t], t=knots, k=3)
                ysmooth = interpolate.splev(distances[h:t], tck)
                self.roi_mtf_value[roi_position][region][channel]['interp_distances'] = np.linspace(distances[h:t][0],
                                                                                                    distances[h:t][-1],
                                                                                                    500)
                self.roi_mtf_value[roi_position][region][channel]['interp_values'] = np.interp(
                    self.roi_mtf_value[roi_position][region][channel]['interp_distances'], distances[h:t], ysmooth)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at esf_calculation function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def lsf_calculation(self, roi_position, region):
        try:
            """This function calculates LSF from the obtained ESF.
            Inputs: 1. roi_position
                    2. region"""
            for channel in self.channels:
                lsf_dividend = np.diff(self.roi_mtf_value[roi_position][region][channel]['interp_values'])
                lsf_divisor = np.diff(self.roi_mtf_value[roi_position][region][channel]['interp_distances'])

                lsf_values = np.divide(lsf_dividend, lsf_divisor)
                self.roi_mtf_value[roi_position][region][channel]['lsf_distances'] \
                    = self.roi_mtf_value[roi_position][region][channel]['interp_distances'][0:-1]
                self.roi_mtf_value[roi_position][region][channel]['lsf_values'] = lsf_values / (max(lsf_values))
                start = int(len(self.roi_mtf_value[roi_position][region][channel]['lsf_values']) * 0.05)
                end = int(len(self.roi_mtf_value[roi_position][region][channel]['lsf_values']) * 0.95)
                self.roi_mtf_value[roi_position][region][channel]['lsf_distances'] = \
                    self.roi_mtf_value[roi_position][region][channel]['lsf_distances'][start:end]
                self.roi_mtf_value[roi_position][region][channel]['lsf_values'] = \
                    self.roi_mtf_value[roi_position][region][channel]['lsf_values'][start:end]
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at lsf_calculation function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def mtf_calculation(self, roi_position, region):
        try:
            """This function calculates the MTF values and the MTF50 is obtained by interpolating the MTF values
            (This is done to obtain the precise MTF50).
            Inputs: 1. roi_position
                    2. region"""
            for channel in self.channels:
                self.roi_mtf_value[roi_position][region][channel]['mtf_values'] = abs(
                    np.fft.fft(self.roi_mtf_value[roi_position][region][channel]['lsf_values'])) / np.sum(
                    self.roi_mtf_value[roi_position][region][channel]['lsf_values'])
                self.roi_mtf_value[roi_position][region][channel]['mtf_distances'] = np.arange(0, np.size(
                    self.roi_mtf_value[roi_position][region][channel]['lsf_distances'])) / (
                                                                                             self.roi_mtf_value[
                                                                                                 roi_position][region][
                                                                                                 channel][
                                                                                                 'lsf_distances'][-1] -
                                                                                             self.roi_mtf_value[
                                                                                                 roi_position][region][
                                                                                                 channel][
                                                                                                 'lsf_distances'][0])
                self.roi_mtf_value[roi_position][region][channel]['mtf_interp_distances'] = np.linspace(0, 1, 100)

                mtf_interp = interpolate.interp1d(self.roi_mtf_value[roi_position][region][channel]['mtf_distances'],
                                                  self.roi_mtf_value[roi_position][region][channel]['mtf_values'],
                                                  kind='cubic')
                self.roi_mtf_value[roi_position][region][channel]['mtf_interp_values'] = mtf_interp(
                    self.roi_mtf_value[roi_position][region][channel]['mtf_interp_distances'])

                self.roi_mtf_value[roi_position][region][channel]['nyquist_value'] = \
                    self.roi_mtf_value[roi_position][region][channel]['mtf_interp_values'][50]
                mtf50 = None
                below_50_indices = np.where(self.roi_mtf_value[roi_position][region][channel]['mtf_interp_values'] < 0.5)[0]
                if len(below_50_indices) > 0:
                    """Find the first index where MTF drops below 50%"""
                    first_below_50_index = below_50_indices[0]
                    """Ensure not at the start to have a point before it"""
                    if first_below_50_index > 0:
                        """Linearly interpolate to find the exact MTF50 point"""
                        x1 = self.roi_mtf_value[roi_position][region][channel]['mtf_interp_distances'][first_below_50_index - 1]
                        y1 = self.roi_mtf_value[roi_position][region][channel]['mtf_interp_values'][first_below_50_index - 1]
                        x2 = self.roi_mtf_value[roi_position][region][channel]['mtf_interp_distances'][first_below_50_index]
                        y2 = self.roi_mtf_value[roi_position][region][channel]['mtf_interp_values'][first_below_50_index]
                        """Linear interpolation formula"""
                        mtf50 = x1 + (x2 - x1) * ((0.5 - y1) / (y2 - y1))
                for index, value in enumerate(self.roi_mtf_value[roi_position][region][channel]['mtf_interp_values']):
                    if value < 0.5:
                        if mtf50:
                            self.roi_mtf_value[roi_position][region][channel]['mtf50'] = mtf50
                        else:
                            self.roi_mtf_value[roi_position][region][channel]['mtf50'] = \
                                self.roi_mtf_value[roi_position][region][channel]['mtf_interp_distances'][index]
                        break
                else:
                    self.roi_mtf_value[roi_position][region][channel]['mtf50'] = \
                        self.roi_mtf_value[roi_position][region][channel]['mtf_interp_distances'][-1]

                for index, value in enumerate(self.roi_mtf_value[roi_position][region][channel]['mtf_interp_values']):
                    if value < 0.2:
                        self.roi_mtf_value[roi_position][region][channel]['mtf20'] = \
                            self.roi_mtf_value[roi_position][region][channel]['mtf_interp_distances'][index]
                        break
                else:
                    self.roi_mtf_value[roi_position][region][channel]['mtf20'] = \
                        self.roi_mtf_value[roi_position][region][channel]['mtf_interp_distances'][-1]

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at mtf_calculation function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))


class ROISelection:
    """This class is used for ROI selection"""
    def __init__(self, input_image, cropped_area_coordinate, setup, roi_frame):
        try:
            """This function splits the obtained ROI and creates two threads to process the ROIs
            Inputs: 1. input_image
                    2. cropped_area_coordinate - ROI coordinates
                    3. setup - Collimator or Relay
                    4. roi_frame"""
            self.detect = None
            self.laplacian = None
            self.org_image = input_image
            self.roi_frame = roi_frame
            self.image = roi_frame.copy()
            for j, k in cropped_area_coordinate.items():
                radius = int(math.sqrt(abs(self.image.shape[1] // 2 - (k[2] + (k[3] - k[2]) // 2)) ** 2
                                       + abs(self.image.shape[0] // 2 - (k[0] + (k[1] - k[0]) // 2)) ** 2))
                if radius != 0:
                    try:
                        radian = math.atan(abs(self.image.shape[0] // 2 - (k[0] + (k[1] - k[0]) // 2)) /
                                           abs(self.image.shape[1] // 2 - (k[2] + (k[3] - k[2]) // 2)))
                    except ZeroDivisionError:
                        logger.error("ZeroDivisionError was occurred in the center ROI.")
                    cv2.circle(self.image, (self.image.shape[1] // 2, self.image.shape[0] // 2), radius, (0, 255, 255), 2)
                    cv2.line(self.image, (self.image.shape[1] // 2, self.image.shape[0] // 2),
                             (int(k[2] + (k[3] - k[2]) // 2), int(k[0] + (k[1] - k[0]) // 2)), (0, 255, 255), 2)

            self.cropped_roi = {}
            thread_one = list(cropped_area_coordinate.keys())[:int(len(cropped_area_coordinate.keys()) / 2)]
            thread_two = list(cropped_area_coordinate.keys())[int(len(cropped_area_coordinate.keys()) / 2):]
            thread_1 = threading.Thread(target=self.run_thread, args=[thread_one, cropped_area_coordinate, setup])
            thread_1.start()
            thread_2 = threading.Thread(target=self.run_thread, args=[thread_two, cropped_area_coordinate, setup])
            thread_2.start()
            thread_1.join()
            thread_2.join()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at ROISelection init function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def run_thread(self, coordinates, cropped_area_coordinate, setup):
        try:
            """This function draws the ROIs for the SFRs and calls the find_roi function
            Inputs: 1. coordinates
                    2. cropped_area_coordinate
                    3. setup - Collimator or Relay"""

            for j in coordinates:
                k = cropped_area_coordinate[j]
                cropped_area = self.roi_frame[k[0]:k[1], k[2]:k[3], :]
                self.cropped_roi[j] = []

                cv2.rectangle(self.image, tuple([k[2], k[0]]), tuple([k[3], k[1]]), (0, 255, 255), 2)
                self.find_roi(cropped_area, j, k, setup)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at ROISelection run_thread function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    @staticmethod
    def get_triangle_point(detect, sfr_peri):
        try:
            """This function is used to find the boundary points of the SFR reg.
            Inputs: 1. detect - Output of Harris corner detector
                    2. sfr_peri - Edge coordinates of SFR reg"""
            triangle = []
            for x in sfr_peri:
                for i, j in zip(np.where(detect > 0.1 * detect.max())[0],
                                np.where(detect > 0.1 * detect.max())[1]):
                    if i == x[0][1] and j == x[0][0]:
                        triangle.append(x[0])
                        # print(i, j)
                        break
            if len(triangle) != 3:
                return None
            else:
                return triangle

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at get_triangle_point function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    @staticmethod
    def detect_roi(centre, side, thresh=0.2):
        try:
            """This function is used to extract roi points and set roi dimensions
            Inputs: 1. center - SFR center
                    2. side - Entire edge
                    3. thresh - to set dimensions for ROI"""
            dist_x = centre[0] - side[0]
            dist_y = centre[1] - side[1]
            maxi = 1 - thresh
            mini = thresh
            if dist_x == 0:
                return None
            rad = math.atan(dist_y / dist_x)
            angle = math.degrees(rad)
            if (-1 <= angle < 1) or (30 <= angle < 60) or (-30 >= angle > -60) or (89 <= angle < 91) or \
                    (-89 >= angle > -91):
                logger.debug("SFRreg chart angle is not accepted angle")
                return None
            else:
                if abs(dist_x) > abs(dist_y):
                    pt_ct_x1 = centre[0] - dist_x * mini
                    pt_ct_x2 = centre[0] - dist_x * maxi
                    # print(pt_ct_x1, pt_ct_x2)
                    pt_ct_y1 = centre[1] - math.tan(rad) * dist_x * mini
                    pt_ct_y2 = centre[1] - math.tan(rad) * dist_x * maxi
                    # print(pt_ct_y1, pt_ct_y2)
                    if pt_ct_y1 > pt_ct_y2:
                        pt_y22 = pt_ct_y1 + abs(dist_x) * 0.2
                        pt_y11 = pt_ct_y2 - abs(dist_x) * 0.2

                    else:
                        pt_y11 = pt_ct_y1 - abs(dist_x) * 0.2
                        pt_y22 = pt_ct_y2 + abs(dist_x) * 0.2

                    if pt_ct_x1 > pt_ct_x2:
                        pt_x22 = pt_ct_x1
                        pt_x11 = pt_ct_x2

                    else:
                        pt_x11 = pt_ct_x1
                        pt_x22 = pt_ct_x2
                else:
                    pt_ct_y1 = centre[1] - dist_y * mini
                    pt_ct_y2 = centre[1] - dist_y * maxi
                    # print(pt_ct_y1, pt_ct_y2)
                    pt_ct_x1 = centre[0] - (dist_y * mini) / math.tan(rad)
                    pt_ct_x2 = centre[0] - (dist_y * maxi) / math.tan(rad)
                    # print(pt_ct_x1, pt_ct_x2)

                    if pt_ct_x1 > pt_ct_x2:
                        pt_x22 = pt_ct_x1 + abs(dist_y) * 0.2
                        pt_x11 = pt_ct_x2 - abs(dist_y) * 0.2

                    else:
                        pt_x11 = pt_ct_x1 - abs(dist_y) * 0.2
                        pt_x22 = pt_ct_x2 + abs(dist_y) * 0.2

                    if pt_ct_y1 > pt_ct_y2:
                        pt_y11 = pt_ct_y2
                        pt_y22 = pt_ct_y1

                    else:
                        pt_y11 = pt_ct_y1
                        pt_y22 = pt_ct_y2

                return np.array([[pt_x11, pt_y11], [pt_x22, pt_y22]], dtype=np.int64)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at detect_roi function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))
            print("Error at detect_roi function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

    def find_roi(self, cropped_area, j, k, setup):
        try:
            """This function finds the individual edges from the SFR chart, calls the detect_roi function and the 
            get_triangle_point function for intermediate processing.
            Inputs: 1. cropped_roi - Cropper ROI
                    2. j, k - coordinates
                    3. setup - Collimator or Relay"""

            """Convert to grayscale."""
            gray = cv2.cvtColor(cropped_area, cv2.COLOR_BGR2GRAY)

            """Apply Gaussian blur method to get proper shape of edge"""
            gaussian = cv2.GaussianBlur(np.uint8(gray), (5, 5), 0)

            """Apply threshold"""
            if setup == 'Collimator station':
                _, thresh = cv2.threshold(gaussian, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            elif setup == 'Relay station':
                _, thresh = cv2.threshold(gaussian, 0, 255,
                                          cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # Binary_inv for relay
            else:
                logger.debug("Setup type is incorrect {}".format(setup))
                return None
            """Apply the erode method to get proper SFR and remove noise"""
            kernel_size = [(3, 3), (5, 5), (7, 7), (9, 9), (11, 11),
                           (15, 15)]
            """Remove kernel size[(11, 11), (15, 15)] to reduce the time(6ms)"""
            for k_size in kernel_size:
                kernel = np.ones(k_size, dtype=np.uint8)
                erode = cv2.erode(thresh, kernel, iterations=2)
                contour = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                contours = imutils.grab_contours(contour)
                contour_count = 0
                for c in contours:
                    area = cv2.contourArea(c)
                    if 500 < area < 5000000:
                        perimeter = cv2.arcLength(c, True)
                        approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
                        if len(approx) == 4 or len(approx) == 5:
                            contour_count += 1

                if contour_count == 2:
                    break

            else:
                logger.debug("SFRreg chart in the position {}: contour count {}".format(j, contour_count))
                return None

            """Apply corner detection"""
            detect = cv2.cornerHarris(erode, 15, 25, 0.04)
            detect = cv2.morphologyEx(detect, cv2.MORPH_DILATE, np.ones((5, 5), dtype=np.uint8))
            sfr_corner_list = []
            for c in contours:
                area = cv2.contourArea(c)
                if 500 < area < 5000000:
                    perimeter = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
                    sfr_corner_list.append(approx)

            for peri in sfr_corner_list:
                triangle_list = self.get_triangle_point(detect, peri)
                if triangle_list:
                    dist_0_1 = math.sqrt(abs(triangle_list[0][1] - triangle_list[1][1]) ** 2 + abs(
                        triangle_list[0][0] - triangle_list[1][0]) ** 2)
                    dist_1_2 = math.sqrt(abs(triangle_list[2][1] - triangle_list[1][1]) ** 2 + abs(
                        triangle_list[2][0] - triangle_list[1][0]) ** 2)
                    dist_0_2 = math.sqrt(abs(triangle_list[0][1] - triangle_list[2][1]) ** 2 + abs(
                        triangle_list[0][0] - triangle_list[2][0]) ** 2)

                    if dist_0_1 > dist_0_2 and dist_0_1 > dist_1_2:
                        centre = triangle_list[2]
                        sides = triangle_list[:2]
                    elif dist_0_2 > dist_0_1 and dist_0_2 > dist_1_2:
                        centre = triangle_list[1]
                        sides = [triangle_list[0], triangle_list[2]]
                    elif dist_1_2 > dist_0_1 and dist_1_2 > dist_0_2:
                        centre = triangle_list[0]
                        sides = triangle_list[1:]
                    else:
                        logger.debug('Incorrect SFRreg Chart')
                        continue

                    for side in sides:
                        roi = self.detect_roi(centre, side)
                        if roi is None:
                            logger.debug("Incorrect angle of slanted edge")
                            c = [int(centre[0] + k[2]), int(centre[1] + k[0])]
                            cv2.line(self.image, tuple([int(centre[0] + k[2]), int(centre[1] + k[0])]),
                                     tuple([side[0] + k[2], side[1] + k[0]]), (0, 0, 255), 2)
                        else:
                            p_1 = roi[0]
                            p_2 = roi[1]

                            rect_roi = np.array([thresh[p_1[1], p_1[0]], thresh[p_1[1], p_2[0]], thresh[p_2[1], p_2[0]],
                                                 thresh[p_2[1], p_1[0]]])

                            if len(rect_roi[rect_roi == 0]) == 2 and len(rect_roi[rect_roi == 255]) == 2:
                                if abs(p_2[1] - p_1[1]) < 30 or abs(p_2[0] - p_1[0]) < 30:
                                    logger.debug('ROI size is less than 30px in position {}: {} {}'.
                                                 format(j, abs(p_2[1] - p_1[1]), abs(p_2[0] - p_1[0])))
                                    cv2.rectangle(self.image, tuple([p_1[0] + k[2], p_1[1] + k[0]]),
                                                  tuple([p_2[0] + k[2], p_2[1] + k[0]]), (0, 0, 255), 2)
                                else:
                                    self.cropped_roi[j].append({'roi_img': self.org_image[p_1[1] + k[0]:p_2[1] + k[0],
                                                                           p_1[0] + k[2]:p_2[0] + k[2]],
                                                                'roi_pt': [[p_1[0] + k[2], p_1[1] + k[0]],
                                                                           [p_2[0] + k[0], p_2[1] + k[0]]]})
                                    cv2.rectangle(self.image, tuple([p_1[0] + k[2], p_1[1] + k[0]]),
                                                  tuple([p_2[0] + k[2], p_2[1] + k[0]]), (255, 255, 0), 2)

                            else:
                                roi = self.detect_roi(centre, side, thresh=0.3)
                                p_1 = roi[0]
                                p_2 = roi[1]
                                rect_roi = np.array(
                                    [thresh[p_1[1], p_1[0]], thresh[p_1[1], p_2[0]], thresh[p_2[1], p_2[0]],
                                     thresh[p_2[1], p_1[0]]])

                                if len(rect_roi[rect_roi == 0]) == 2 and len(rect_roi[rect_roi == 255]) == 2:
                                    if abs(p_2[1] - p_1[1]) < 30 or abs(p_2[0] - p_1[0]) < 30:
                                        logger.debug('ROI size is less than 30px in position {}: {} {}'.
                                                     format(j, abs(p_2[1] - p_1[1]), abs(p_2[0] - p_1[0])))
                                        cv2.rectangle(self.image, tuple([p_1[0] + k[2], p_1[1] + k[0]]),
                                                      tuple([p_2[0] + k[2], p_2[1] + k[0]]), (0, 0, 255), 2)
                                    else:
                                        self.cropped_roi[j].append(
                                            {'roi_img': self.org_image[p_1[1] + k[0]:p_2[1] + k[0],
                                                        p_1[0] + k[2]:p_2[0] + k[2]],
                                             'roi_pt': [[p_1[0] + k[2], p_1[1] + k[0]],
                                                        [p_2[0] + k[0], p_2[1] + k[0]]]})
                                        cv2.rectangle(self.image, tuple([p_1[0] + k[2], p_1[1] + k[0]]),
                                                      tuple([p_2[0] + k[2], p_2[1] + k[0]]), (255, 255, 0), 2)

                                else:
                                    logger.debug('incorrect ROI')

                else:
                    logger.debug('Incorrect SFRreg Chart')

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error("Error at find_roi function : {}|{}|{}|{}".format(exc_type, fname, exc_tb.tb_lineno, e))

