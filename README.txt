markdown
# 📌 Шпаргалка по запуску проекта Educa (Windows)

Все команды выполняются в терминале (PowerShell) **из корневой папки проекта** (там, где лежит файл `docker-compose.yml`).

### 🚀 Запуск проекта

Для первого запуска или если менялись файлы `requirements.txt` / `Dockerfile`:
```powershell
$env:DOCKER_BUILDKIT=0; $env:COMPOSE_DOCKER_CLI_BUILD=0; docker-compose up --build
Для обычного повседневного запуска (если ничего не менял в зависимостях):

powershell
docker-compose up
🛑 Остановка проекта
Нажми Ctrl + C в терминале, где запущен проект.

Чтобы полностью удалить контейнеры (например, если что-то зависло):

powershell
docker-compose down
🗄️ Работа с базой данных (миграции)
Если база данных пустая или ты добавил новые модели (например, в models.py), нужно применить миграции. Выполняется в отдельном терминале, пока основной проект запущен:

powershell
docker-compose run --rm daphne sh -c "cd /code/educa && python manage.py migrate"
👤 Создание пользователя (админа)
Чтобы зайти в панель администратора (http://localhost:9001/admin/):

powershell
docker-compose run --rm daphne sh -c "cd /code/educa && python manage.py createsuperuser"
Система попросит ввести имя пользователя, email (можно пропустить) и пароль. При вводе пароля символы не отображаются — это нормально.

🎨 Сбор статики (CSS, JS, картинки)
Если пропали стили или ты добавил новые картинки в static/:

powershell
docker-compose run --rm daphne sh -c "cd /code/educa && python manage.py collectstatic --noinput"
(После этого обнови страницу в браузере через Ctrl + F5)

🛠️ Полезные команды Django
Любую команду manage.py можно запустить по аналогии с миграциями:

Открыть консоль Python внутри Django:

powershell
docker-compose run --rm daphne sh -c "cd /code/educa && python manage.py shell"
Создать резервную копию базы (SQLite):

powershell
docker-compose run --rm daphne sh -c "cd /code/educa && cp db.sqlite3 db_backup.sqlite3"
🌐 Куда заходить в браузере
Сам сайт: http://localhost:9001

Админка: http://localhost:9001/admin/ (после создания суперпользователя)

http://192.168.2.94:9001/


💡 Важное правило: Если ты меняешь код Python (.py файлы), Daphne подхватит изменения автоматически (если включен autoreload). Если меняешь requirements.txt — обязательно пересобирай с флагом --build.