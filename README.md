# scrape-and-analyses

Bu proje, çeşitli haber kaynaklarından veri çekme, bu verileri analiz etme ve sonuçları görselleştirme işlevlerini gerçekleştirir. Proje, haber verilerini MongoDB'ye kaydeder, kelime frekansı analizi yapar ve bu analizleri hem grafik hem de bulut formatında görselleştirir. Ayrıca, projede detaylı loglama bulunmaktadır.

# Kurulum
Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları takip edin:

Önkoşullar
Bu projeyi çalıştırmadan önce aşağıdaki araçların yüklü olması gerekmektedir:

Python 3.8 veya üzeri
Docker ve Docker Compose (MongoDB ve uygulama konteynerleri için)
NLTK veri setleri (kelime analizi için)
Kurulum Adımları
1)Projeyi klonlayın:
git clone 
cd yourproject
2)Gerekli Python paketlerini yükleyin:

pip install -r requirements.txt
3)Docker Compose ile uygulamayı ve MongoDB'yi başlatın:

docker-compose up --build
# Kullanım
Uygulama başlatıldıktan sonra, tarayıcınızda [localhost:8000](http://127.0.0.1:8000/) adresine giderek uygulamayı kullanabilirsiniz.

# Ana Özellikler
Haber Veri Çekme: Belirli bir URL'den haber verilerini çeker.
Kelime Frekansı Analizi: Toplanan haber verilerindeki en sık kullanılan kelimeleri analiz eder.
Görselleştirme: Kelime frekansını bar grafiği ve kelime bulutu olarak görselleştirir.
Veri Kaydetme: Çekilen haber verilerini ve analiz sonuçlarını MongoDB'ye kaydeder.
Analiz Edilen Veri ve Kelime Frekansı Grafiği
Analiz Edilen Veri: Haber metinleri ve meta verileri.
Kelime Frekansı Grafiği: Haber metinlerinde en sık kullanılan 10 kelimenin frekansını gösterir.
# Log Bilgileri
Uygulama, işlemler sırasında detaylı loglar üretir. Bu loglar, hata ayıklama ve sistem izleme için kullanılabilir.

# Dokümantasyon
Projedeki her fonksiyon ve sınıf, işlevlerini ve parametrelerini açıklayan docstrings ile dokümante edilmiştir.
