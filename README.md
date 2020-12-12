#### Паук для сбора информации об объектах недвижимости с Zillow.com
Установка:<br>
pip install -r requirements.txt<br>
Необходимо установить [geckodriver](https://github.com/mozilla/geckodriver/releases/)<br>
Создать файл config.py в директории spiders с параметром region = 'oshkosh-wi'<br>
Запуск:<br>
python main.py <br>
Паук получает список локаций из config.py.<br>
Обходит все объявления<br>
Из каждого объявления извлекает:<br>
1. price - Цена указанная в объявлении
2. address - Поле адреса указанное в объявлении
3. photos - Все фотографии из объявления в максимальном разрешении
4. Скачивает фотографии на компьютере
