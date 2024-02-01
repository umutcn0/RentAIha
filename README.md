# Getting Started
İHA Kiralama Projesi, İnsansız Hava Araçları'nın (İHA) kiralama işlemlerini yöneten bir web uygulamasıdır. Proje, Python dilinde Django web framework'ü kullanılarak geliştirilmiştir.

### Prerequisites
- Python 3.11.x
- PostgreSQL
- Django

### Installation
- Uygulamayı çalıştırmadan önce PostgreSQL üzerinde bir veritabanı oluşturmanız gerekli.
- Daha sonra Virtual enviroment oluşturunuz ve dosya içerisindeki gereklilikleri yükleyiniz.
- "rentAIha" dosyası içerisine .env dosyası oluturmalı ve aşağıdaki verileri yazmalısınız:

```python
SECRET_KEY=YOUR_SECRET_KEY
DB_NAME=YOUR_DB_NAME
DB_USER=YOUR_DB_USER
DB_PASSWORD=YOUR_DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432
```
- Ve uygulamayı çalıştıramaya hazırsınız.

### Notes
- **Postman collection dosyasını uygulamanızda içe aktararak gerekli endpointlere erişebilir ve kullanabilirsiniz.**
- **Uygulama içerisinde "manage.py test" yazarak uygulamada yazılı olan testleri kullanabilirsiniz.**

### How It Works
Projenin ana fonksiyonaliteleri arasında kullanıcı üyelik ve giriş ekranı, İHA yönetimi (ekleme, silme, güncelleme, listeleme, kiralama), üyelerin İHA kiralama kayıtları, kiralanan İHA yönetimi özellikleri bulunmaktadır.

# Authors
- Umut Can - [linkedin](https://www.linkedin.com/in/umut-can-0a7417157/)
