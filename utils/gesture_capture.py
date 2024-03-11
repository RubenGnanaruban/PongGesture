import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector
import math


class HandToPaddle:

    def __init__(self, hand_resting_height=0.25):
        # self.paddle_half_h = 10   # Not needed
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=1)

        self.success, self.img = self.cap.read()
        self.img_h, self.img_w, _ = self.img.shape

        # Let's change the resting hand to the lower potion of the webcam for
        # better ergonomics
        self.hand_neutral_height = int(self.img_h * (1-hand_resting_height))
        self.focus_factor = 50000
        self.depth_cutoff = 900

    def update2d(self, hand_speed=3):
        self.success, self.img = self.cap.read()
        if self.success:
            hand, self.img = self.detector.findHands(self.img, draw=False)
            if hand:
                _, hand_height = hand[0]["center"]
                hand_from_center = hand_height - self.hand_neutral_height
                paddle_y = int(self.hand_neutral_height
                               + hand_from_center * hand_speed)
                return paddle_y
            return False

    def update3d(self, hand_speed=4):
        self.success, self.img = self.cap.read()
        if self.success:
            hand, self.img = self.detector.findHands(self.img, draw=False)
            if hand:
                _, hand_height = hand[0]["center"]
                hand_from_center = hand_height - self.hand_neutral_height
                paddle_y = int(self.hand_neutral_height
                               + hand_from_center * hand_speed)
                bbox = hand[0]["bbox"]
                pad_z = self.depth_cutoff - int(self.focus_factor /
                                                math.sqrt(bbox[2] * bbox[3]))
                return paddle_y, pad_z
            return False

    def get_camera_to_mouse(self, screen_width, screen_height):
        # This module is used at the menu screen.
        # When a hand is detected the location of the tip of the index
        # finger is converted to usable mouse coordinates. Touching the tips
        # of index finger and thumb makes the mouse to click.
        self.success, self.img = self.cap.read()
        hand_neutral_y = int(self.img_h * 0.4)
        hand_neutral_x = int(self.img_w / 2)
        motion_amplifier = 3  # use a different hand_speed_factor here
        if self.success:
            hand, self.img = self.detector.findHands(self.img, draw=False)
            if hand:
                x, y, _ = hand[0]["lmList"][8]
                # x, y = hand[0]["center"]
                # flip around vertical for mirroring
                hand_from_center_x = hand_neutral_x - x
                hand_from_center_y = y - hand_neutral_y
                mouse_x = int(screen_width / 2
                              + hand_from_center_x * motion_amplifier)
                mouse_y = int(screen_height / 2
                              + hand_from_center_y * motion_amplifier)

                mouse_out_x = max(0, min(mouse_x, screen_width))
                mouse_out_y = max(0, min(mouse_y, screen_height))

                thumb_x, thumb_y, _ = hand[0]["lmList"][4]
                length, info, _ = (
                    self.detector.findDistance((thumb_x, thumb_y),
                                               (x, y)))
                if length / hand[0]["bbox"][2] < 0.2:
                    pyautogui.click()
                return [mouse_out_x, mouse_out_y]
            return False

    def set_gesture_preferences_3d(self, hand_speed=3):
        self.success, self.img = self.cap.read()
        if self.success:
            hand, self.img = self.detector.findHands(self.img, draw=False)
            if hand:
                _, hand_height = hand[0]["center"]
                hand_from_center = hand_height - self.hand_neutral_height
                paddle_y = int(self.hand_neutral_height
                               + hand_from_center * hand_speed)
                bbox = hand[0]["bbox"]
                pad_z = self.depth_cutoff - int(self.focus_factor /
                                                math.sqrt(bbox[2] * bbox[3]))
                return paddle_y, pad_z
            cv2.imshow("cam", self.img)
            return False


class Hands2ToPaddles:

    def __init__(self, hand_speed=3, hand_resting_height=0.25):
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=2)

        self.success, self.img = self.cap.read()
        self.img_h, self.img_w, _ = self.img.shape

        # Let's change the resting hand to the lower potion of the webcam for
        # better ergonomics
        self.hand_neutral_height = int(self.img_h * (1-hand_resting_height))
        self.hand_speed = hand_speed
        self.focus_factor = 50000
        self.depth_cutoff = 900

    def update2d(self):
        self.success, self.img = self.cap.read()
        paddles_y = [False, False]
        if self.success:
            hands, self.img = self.detector.findHands(self.img, draw=False)
            for hand in hands:
                if hand:
                    hand_x, hand_height = hand["center"]
                    hand_from_center = hand_height - self.hand_neutral_height
                    paddle_y = int(self.hand_neutral_height
                                   + hand_from_center * self.hand_speed)
                    if hand_x <= self.img_w / 2:
                        # Player on the right appears on the left side of img
                        paddles_y[0] = paddle_y
                    else:
                        paddles_y[1] = paddle_y

        return paddles_y
