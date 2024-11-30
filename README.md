# PCB_Kusur_Tespit_Algoritmasi
Proje Hakkında
Bu proje, baskı devre kartları (PCB) üzerindeki üretim kusurlarını otomatik olarak tespit etmeyi amaçlamaktadır. Algoritma, bir referans görüntüyü test edilen görüntüyle karşılaştırarak kusurları belirler. Proje, üretim hatalarını hızlı ve doğru bir şekilde analiz etmek için etkili bir çözüm sunar.

Özellikler
Görüntü Hizalama: SIFT algoritması kullanılarak referans ve test görüntüleri arasında homografi matrisi oluşturulur.
Kusur Tespiti: Görüntü fark analizi ve kontur tespiti ile potansiyel kusurlar belirlenir.
Kusur Karşılaştırması: Tespit edilen kusurlar, etiketlenmiş verilerle doğruluk ve geri çağırma oranları hesaplanarak karşılaştırılır.
Sonuç Görselleştirme: Tespit edilen kusurlar ve etiketler renkli görsellerle kullanıcıya sunulur.

Kullanılan Teknolojiler
Python
OpenCV
NumPy
Matplotlib
Projenin Çalıştırılması
Gerekli Python kütüphanelerini yükleyin:

pip install opencv-python numpy matplotlib

Projeyi indirip tespit.py dosyasını çalıştırın:

python tespit.py

Referans ve test görüntülerinin yollarını tespit.py dosyasındaki ilgili bölüme ekleyin.
Çalıştırarak kusur tespiti sonuçlarını ve görselleştirmeleri gözlemleyin.
 
Sonuçlar ve Çıkarımlar 

Algoritma, çeşitli PCB kusurlarını (%85 doğruluk ve %90 geri çağırma oranıyla) başarıyla tespit edebilmiştir. Ancak, görüntü kalitesi ve aydınlatma değişiklikleri doğruluk oranını etkileyebilir.
