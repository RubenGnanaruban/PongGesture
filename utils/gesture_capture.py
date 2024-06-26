import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector
import math
from threading import Thread  #, Event
# import time

hand_resting_height = 0.25
focus_factor = 50000
depth_cutoff = 900
hand_speed = [3, 4, 3, 4]


class HandToPaddle:

    def __init__(self, max_hands_to_detect=1):
        # self.event_roll = Event()
        # self.event_process = Event()
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=max_hands_to_detect)

        self.img_1 = None
        self.flag_img_write = True
        success, self.img_0 = self.cap.read()
        if success:
            self.img_h, self.img_w, _ = self.img_0.shape
        else:
            print("[Exiting]: Error accessing webcam.")
            exit(0)

        self.hand_neutral_height = int(self.img_h * (1 - hand_resting_height))
        self.paddle_y = False
        self.paddle_z = False

    def capture_image(self):
        # self.event_roll.wait()
        if self.flag_img_write:
            success, self.img_1 = self.cap.read()
        else:
            success, self.img_0 = self.cap.read()
        if not success:
            print("[Exiting]: Error accessing webcam.")
        # self.event_roll.clear()

    def __hand_1d_from_image(self, img):
        hand, img = self.detector.findHands(img, draw=False)
        if hand:
            _, hand_height = hand[0]["center"]
            hand_from_center = (hand_height - self.hand_neutral_height)
            self.paddle_y = int(self.hand_neutral_height
                                + hand_from_center * hand_speed[0])
        else:
            self.paddle_y = False

    def __capture_hand_1d(self):
        # self.event_process.wait()
        if self.flag_img_write:
            # img_0 can be accessed thread-safe
            self.__hand_1d_from_image(self.img_0)
        else:
            # img_1 can be accessed thread-safe
            self.__hand_1d_from_image(self.img_1)
        # self.event_process.clear()

    def update2d(self):
        thread_cap = Thread(target=self.capture_image, args=(),
                            daemon=True)
        thread_pro = Thread(target=self.__capture_hand_1d(), args=(),
                            daemon=True)
        thread_cap.start()
        thread_pro.start()
        thread_cap.join()
        thread_pro.join()
        self.flag_img_write = not self.flag_img_write
        return self.paddle_y

    def __hand_3d_from_image(self, img):
        hand, img = self.detector.findHands(img, draw=False)
        if hand:
            _, hand_height = hand[0]["center"]
            hand_from_center = (hand_height - self.hand_neutral_height)
            self.paddle_y = int(self.hand_neutral_height
                                + hand_from_center * hand_speed[0])
            bbox = hand[0]["bbox"]
            self.paddle_z = depth_cutoff - int(focus_factor /
                                               math.sqrt(bbox[2] * bbox[3]))
        else:
            self.paddle_y = False
            self.paddle_z = False

    def __capture_hand_3d(self):
        if self.flag_img_write:
            # img_0 can be accessed thread-safe
            self.__hand_3d_from_image(self.img_0)
        else:
            # img_1 can be accessed thread-safe
            self.__hand_3d_from_image(self.img_1)

    def update3d(self):
        thread_cap = Thread(target=self.capture_image, args=(),
                            daemon=True)
        thread_pro = Thread(target=self.__capture_hand_3d(), args=(),
                            daemon=True)
        thread_cap.start()
        thread_pro.start()
        thread_cap.join()
        thread_pro.join()
        self.flag_img_write = not self.flag_img_write
        return self.paddle_y, self.paddle_z

    def __hand_2d_from_image(self, img, screen_width, screen_height):
        hand_neutral_y = int(self.img_h * 0.4)
        hand_neutral_x = int(self.img_w / 2)
        motion_amplifier = 3  # use a different hand_speed_factor here
        hand, img = self.detector.findHands(img, draw=False)
        if hand:
            x, y, _ = hand[0]["lmList"][8]

            # flip around vertical for mirroring
            hand_from_center_x = hand_neutral_x - x
            hand_from_center_y = y - hand_neutral_y
            mouse_x = int(screen_width / 2
                          + hand_from_center_x * motion_amplifier)
            mouse_y = int(screen_height / 2
                          + hand_from_center_y * motion_amplifier)
            self.paddle_z = max(0, min(mouse_x, screen_width - 1))
            self.paddle_y = max(0, min(mouse_y, screen_height - 1))
            thumb_x, thumb_y, _ = hand[0]["lmList"][4]
            length, info, _ = (
                self.detector.findDistance((thumb_x, thumb_y), (x, y)))
            if length / hand[0]["bbox"][2] < 0.2:
                pyautogui.click()

        else:
            self.paddle_y = False
            self.paddle_z = False

    def __capture_hand_mouse(self, screen_width, screen_height):
        # self.event_process.wait()
        if self.flag_img_write:
            # img_0 can be accessed thread-safe
            self.__hand_2d_from_image(self.img_0, screen_width, screen_height)
        else:
            # img_1 can be accessed thread-safe
            self.__hand_2d_from_image(self.img_1, screen_width, screen_height)

    def update_mouse_from_webcam(self, screen_width, screen_height):
        thread_cap = Thread(target=self.capture_image, args=(),
                            daemon=True)
        thread_pro = Thread(target=self.__capture_hand_mouse,
                            args=(screen_width, screen_height),
                            daemon=True)
        thread_cap.start()
        thread_pro.start()
        thread_cap.join()
        thread_pro.join()
        self.flag_img_write = not self.flag_img_write
        return [self.paddle_z, self.paddle_y]

    def get_camera_to_mouse(self, screen_width, screen_height):
        # This module is used at the menu screen.
        # When a hand is detected the location of the tip of the index
        # finger is converted to usable mouse coordinates. Touching the tips
        # of index finger and thumb makes the mouse to click.
        success, self.img_0 = self.cap.read()
        hand_neutral_y = int(self.img_h * 0.4)
        hand_neutral_x = int(self.img_w / 2)
        motion_amplifier = 3  # use a different hand_speed_factor here
        if success:
            hand, self.img_0 = self.detector.findHands(self.img_0, draw=False)
            if hand:
                x, y, _ = hand[0]["lmList"][8]

                # flip around vertical for mirroring
                hand_from_center_x = hand_neutral_x - x
                hand_from_center_y = y - hand_neutral_y
                mouse_x = int(screen_width / 2
                              + hand_from_center_x * motion_amplifier)
                mouse_y = int(screen_height / 2
                              + hand_from_center_y * motion_amplifier)

                mouse_out_x = max(0, min(mouse_x, screen_width - 1))
                mouse_out_y = max(0, min(mouse_y, screen_height - 1))

                thumb_x, thumb_y, _ = hand[0]["lmList"][4]
                length, info, _ = (
                    self.detector.findDistance((thumb_x, thumb_y),
                                               (x, y)))
                if length / hand[0]["bbox"][2] < 0.2:
                    pyautogui.click()
                return [mouse_out_x, mouse_out_y]
            return False

    # def set_gesture_preferences_3d(self):
    #     self.success, self.img = self.cap.read()
    #     if self.success:
    #         hand, self.img = self.detector.findHands(self.img, draw=False)
    #         if hand:
    #             _, hand_height = hand[0]["center"]
    #             hand_from_center = hand_height - self.hand_neutral_height
    #             paddle_y = int(self.hand_neutral_height
    #                            + hand_from_center * hand_speed)
    #             bbox = hand[0]["bbox"]
    #             pad_z = self.depth_cutoff - int(self.focus_factor /
    #                                             math.sqrt(bbox[2] * bbox[3]))
    #             return paddle_y, pad_z
    #         cv2.imshow("cam", self.img)
    #         return False


class Hands2ToPaddles(HandToPaddle):

    def __init__(self):
        HandToPaddle.__init__(self, max_hands_to_detect=2)
        self.paddles_y = [False, False]

    def __hand_1d_from_image(self, img):
        hands, img = self.detector.findHands(img, draw=False)
        for hand in hands:
            if hand:
                hand_x, hand_height = hand["center"]
                hand_from_center = (hand_height - self.hand_neutral_height)
                if hand_x <= self.img_w / 2:
                    # Player on the right appears on the left of img
                    self.paddles_y[0] = int(self.hand_neutral_height
                                            + hand_from_center * hand_speed[0])
                else:
                    self.paddles_y[1] = int(self.hand_neutral_height
                                            + hand_from_center * hand_speed[2])
            else:
                self.paddles_y = [False, False]

    def __capture_hand_1d(self):
        # self.event_process.wait()
        if self.flag_img_write:
            # img_0 can be accessed thread-safe
            self.__hand_1d_from_image(self.img_0)
        else:
            # img_1 can be accessed thread-safe
            self.__hand_1d_from_image(self.img_1)

    def update2d(self):
        thread_cap = Thread(target=self.capture_image, args=(),
                            daemon=True)
        thread_pro = Thread(target=self.__capture_hand_1d(), args=(),
                            daemon=True)
        thread_cap.start()
        thread_pro.start()
        thread_cap.join()
        thread_pro.join()
        self.flag_img_write = not self.flag_img_write
        return self.paddles_y
