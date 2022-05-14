import cv2
import mediapipe as mp


def hpt(image):
  mp_hands = mp.solutions.hands
  mp_drawing_styles = mp.solutions.drawing_styles
  mp_drawing = mp.solutions.drawing_utils
  with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

  return image

def od(image):
  mp_object_detection = mp.solutions.object_detection
  mp_drawing = mp.solutions.drawing_utils

  with mp_object_detection.ObjectDetection(
    min_detection_confidence=0.1) as object_detection:

    results = object_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)
  return image

