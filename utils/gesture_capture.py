import cv2
from cvzone.HandTrackingModule import HandDetector


class HandToPaddle:

    def __init__(self, hand_speed=3, hand_resting_height=0.25):
        self.hand_speed_factor = hand_speed
        # self.paddle_half_h = 10
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=1)

        self.success, self.img = self.cap.read()
        self.img_h, self.img_w, _ = self.img.shape

        # Let's change the resting hand to the lower potion of the webcam for
        # better ergonomics
        self.hand_neutral_height = int(self.img_h * (1-hand_resting_height))
        # self.paddle_xl = self.img_w - 10
        # self.paddle_xr = self.img_w - 5

    def update(self):
        self.success, self.img = self.cap.read()
        if self.success:
            hand, self.img = self.detector.findHands(self.img, draw=False)

            if hand:
                _, hand_height = hand[0]["center"]
                hand_from_center = hand_height - self.hand_neutral_height
                paddle_y = int(self.hand_neutral_height
                               + hand_from_center * self.hand_speed_factor)
                # paddle_yl = max(paddle_y - self.paddle_half_h, 0)
                # paddle_yr = min(paddle_y + self.paddle_half_h, self.img_h)
                # cv2.rectangle(self.img, [self.paddle_xl, paddle_yl],
                #               [self.paddle_xr, paddle_yr], (255, 0, 0), -1)
                return paddle_y

            # cv2.imshow("cam", self.img)
            return False
