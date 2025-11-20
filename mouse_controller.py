"""
Mouse kontrolü modülü - El pozisyonlarını mouse hareketine çevirir
"""
import pyautogui
import numpy as np

class MouseController:
    def __init__(self, camera_width, camera_height, smoothing_factor=0.85):
        """
        Args:
            camera_width: Kamera genişliği
            camera_height: Kamera yüksekliği
            smoothing_factor: Mouse hareket yumuşatma faktörü (0-1 arası, yüksek = daha yumuşak)
        """
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.smoothing_factor = smoothing_factor
        
        # Ekran boyutlarını al
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Önceki mouse pozisyonu (smoothing için)
        self.prev_x = self.screen_width // 2
        self.prev_y = self.screen_height // 2
        
        # Tıklama durumu - hysteresis için
        self.is_clicking = False
        self.click_hold_frames = 0  # Tıklama tutma süresi
        self.click_release_frames = 0  # Tıklama bırakma süresi
        self.min_hold_frames = 2  # Tıklama için minimum tutma süresi
        self.min_release_frames = 3  # Bırakmak için minimum süre
        
      
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0
        
        print(f"Mouse kontrolü başlatıldı. Ekran: {self.screen_width}x{self.screen_height}")
    
    def update_mouse_position(self, finger_x, finger_y):
        """
        Parmak pozisyonunu mouse pozisyonuna çevir
        
        Args:
            finger_x: Parmak x pozisyonu (kamera koordinatları)
            finger_y: Parmak y pozisyonu (kamera koordinatları)
        """
        if finger_x is None or finger_y is None:
            return
        
        normalized_x = finger_x / self.camera_width
        normalized_y = finger_y / self.camera_height
        
        screen_x = int(normalized_x * self.screen_width)
        screen_y = int(normalized_y * self.screen_height)
        
        screen_x = max(0, min(self.screen_width - 1, screen_x))
        screen_y = max(0, min(self.screen_height - 1, screen_y))
        
        smooth_x = int(self.prev_x * (1 - self.smoothing_factor) + 
                      screen_x * self.smoothing_factor)
        smooth_y = int(self.prev_y * (1 - self.smoothing_factor) + 
                      screen_y * self.smoothing_factor)
        
        if abs(smooth_x - self.prev_x) > 1 or abs(smooth_y - self.prev_y) > 1:
            try:
                pyautogui.moveTo(smooth_x, smooth_y, duration=0, _pause=False)
            except:
                pass
        
        self.prev_x = smooth_x
        self.prev_y = smooth_y
    
    def handle_click(self, is_click_gesture):
        """
        Tıklama hareketini işle - hysteresis ile daha güvenilir
        
        Args:
            is_click_gesture: Tıklama hareketi yapılıyor mu?
        """
        if is_click_gesture:
            self.click_hold_frames += 1
            self.click_release_frames = 0
            
            if not self.is_clicking and self.click_hold_frames >= self.min_hold_frames:
                try:
                    pyautogui.mouseDown(_pause=False)
                    self.is_clicking = True
                except:
                    pass
        else:
            self.click_release_frames += 1
            self.click_hold_frames = 0
            
            if self.is_clicking and self.click_release_frames >= self.min_release_frames:
                try:
                    pyautogui.mouseUp(_pause=False)
                    self.is_clicking = False
                except:
                    pass

