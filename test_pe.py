import mediapipe as mp
import cv2
from alg import pe
if __name__ == "__main__":
    test_img = cv2.imread("pose.jpeg")
    test_img = pe(test_img)
    cv2.imwrite("pose.jpeg")

