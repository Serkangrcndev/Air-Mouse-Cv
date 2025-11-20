# Air Mouse CV

Kamera ile el takibi kullanarak bilgisayar mouse'unu kontrol etmenizi sağlayan bir Python uygulaması. MediaPipe ve OpenCV kullanarak işaret parmağınızın hareketlerini mouse hareketine çevirir ve başparmak ile işaret parmağınızı birleştirerek tıklama yapmanıza olanak tanır.

## Özellikler

- Gerçek zamanlı el ve parmak takibi
- İşaret parmağı ile mouse kontrolü
- Başparmak ve işaret parmağı birleştirerek tıklama
- Yumuşak ve akıcı mouse hareketleri
- Düşük gecikme ile yüksek performans

## Gereksinimler

- Python 3.7 veya üzeri
- Web kamerası
- Windows, Linux veya macOS

## Kurulum

1. Repository'yi klonlayın:
```bash
git clone https://github.com/Serkangrcndev/air-mouse-cv.git
cd air-mouse-cv
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

Uygulamayı başlatmak için:
```bash
python main.py
```

### Kontroller

- **M tuşu**: Mouse kontrolünü aç/kapat
- **Q tuşu**: Uygulamadan çıkış

### Kullanım Adımları

1. Kameranın önüne geçin ve işaret parmağınızı kameraya doğru tutun
2. İşaret parmağınızı hareket ettirerek mouse'u kontrol edin
3. Başparmak ve işaret parmağınızı birleştirerek tıklama yapın

## Teknik Detaylar

- **El Takibi**: MediaPipe Hands modeli
- **Mouse Kontrolü**: PyAutoGUI
- **Görüntü İşleme**: OpenCV
- **Tıklama Algılama**: 3D mesafe hesaplama ile başparmak ve işaret parmağı birleşme tespiti
- **Yumuşatma**: Exponential smoothing algoritması ile akıcı hareket

## Yapılandırma

`mouse_controller.py` dosyasında şu parametreleri değiştirebilirsiniz:

- `smoothing_factor`: Mouse hareket yumuşatma faktörü (0-1 arası, varsayılan: 0.85)
- `min_hold_frames`: Tıklama için minimum tutma süresi (frame sayısı)
- `min_release_frames`: Tıklamayı bırakmak için minimum süre (frame sayısı)

`hand_tracker.py` dosyasında:

- `min_detection_confidence`: El tespiti için minimum güven eşiği
- Tıklama algılama mesafesi (varsayılan: 0.08)

## Notlar

- Mouse kontrolü aktifken fareyi ekranın köşesine götürürseniz uygulama durur (PyAutoGUI güvenlik özelliği)
- İyi aydınlatma altında daha iyi çalışır
- Kameranın önünde net bir şekilde durun

## Lisans

Bu proje açık kaynaklıdır ve MIT lisansı altında dağıtılmaktadır.

## Katkıda Bulunma

Hata bildirimi ve öneriler için issue açabilirsiniz. Pull request'ler memnuniyetle karşılanır.

