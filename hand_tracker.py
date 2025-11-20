"""
El takibi modülü - MediaPipe kullanarak parmak pozisyonlarını tespit eder
"""
import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def detect_hands(self, frame, draw_landmarks=False):
        """Kameradan gelen frame'de elleri tespit eder"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        landmarks = None
        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]
            if draw_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, landmarks, self.mp_hands.HAND_CONNECTIONS
                )
        
        return landmarks, frame
    
    def get_finger_tip(self, landmarks, frame_shape):
        """İşaret parmağının ucunun pozisyonunu döndürür"""
        if landmarks is None:
            return None
        
        h, w = frame_shape[:2]
        finger_tip = landmarks.landmark[8]
        

        x = int(finger_tip.x * w)
        y = int(finger_tip.y * h)
        
        return (x, y)
    
    def is_click_gesture(self, landmarks):
        """Başparmak ve işaret parmağının birleşip birleşmediğini kontrol eder (tıklama)"""
        if landmarks is None:
            return False
        
  
        index_tip = landmarks.landmark[8]
        thumb_tip = landmarks.landmark[4]
        
        dx = index_tip.x - thumb_tip.x
        dy = index_tip.y - thumb_tip.y
        dz = index_tip.z - thumb_tip.z
        

        distance = (dx**2 + dy**2 + dz**2)**0.5
        

        return distance < 0.08
    
    def release(self):
        """Kaynakları serbest bırak"""
        self.hands.close()

