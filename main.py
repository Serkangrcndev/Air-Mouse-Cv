"""
Ana uygulama - Kamera ile el takibi ve mouse kontrolü
"""
import cv2
import numpy as np
from hand_tracker import HandTracker
from mouse_controller import MouseController

class MouseControlApp:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        
        # Kamera ayarları - daha düşük çözünürlük = daha hızlı işleme
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # FPS'i artır
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Frame boyutlarını al
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Kamera açılamadı!")
        
        self.height, self.width = frame.shape[:2]
        
       
        self.hand_tracker = HandTracker()
        self.mouse_controller = MouseController(self.width, self.height, smoothing_factor=0.85)
        
        self.mouse_control_enabled = True
        
        print("Uygulama başlatıldı!")
        print("Kontroller:")
        print("  - 'M' tuşu: Mouse kontrolünü aç/kapat")
        print("  - 'Q' tuşu: Çıkış")
        print("\nKullanım:")
        print("  - İşaret parmağınızla mouse'u hareket ettirin")
        print("  - Başparmak ve işaret parmağınızı birleştirerek tıklayın")
    
    def run(self):
        """Ana döngü"""
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
       
            frame = cv2.flip(frame, 1)
            
            
            landmarks, frame = self.hand_tracker.detect_hands(frame, draw_landmarks=False)
            finger_tip = self.hand_tracker.get_finger_tip(landmarks, frame.shape)
            is_clicking = self.hand_tracker.is_click_gesture(landmarks)
            

            if self.mouse_control_enabled:
                if finger_tip is not None:
 
                    self.mouse_controller.update_mouse_position(
                        finger_tip[0], finger_tip[1]
                    )
                    

                    self.mouse_controller.handle_click(is_clicking)
                    
                    cv2.circle(frame, finger_tip, 15, (0, 255, 0), 2)
                    

                    if is_clicking:
                        cv2.circle(frame, finger_tip, 20, (0, 0, 255), 3)
                        cv2.putText(frame, "TIKLIYOR", (finger_tip[0] + 25, finger_tip[1]),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            mode_text = "Mouse Kontrol: AÇIK" if self.mouse_control_enabled else "Mouse Kontrol: KAPALI"
            color = (0, 255, 0) if self.mouse_control_enabled else (0, 0, 255)
            cv2.putText(frame, mode_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            if finger_tip is not None:
                cv2.putText(frame, f"Parmak: ({finger_tip[0]}, {finger_tip[1]})", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('m'):
                self.mouse_control_enabled = not self.mouse_control_enabled
                if not self.mouse_control_enabled:
                    print("Mouse kontrolü kapatıldı.")
                else:
                    print("Mouse kontrolü açıldı.")
            
          
            cv2.imshow('El ile Mouse Kontrolü', frame)
        
        self.cleanup()
    
    def cleanup(self):
        """Kaynakları temizle"""
        self.cap.release()
        cv2.destroyAllWindows()
        self.hand_tracker.release()
        print("Uygulama kapatıldı.")

if __name__ == "__main__":
    try:
        app = MouseControlApp()
        app.run()
    except Exception as e:
        print(f"Hata: {e}")
        import traceback
        traceback.print_exc()

