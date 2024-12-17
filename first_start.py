'''создание нового проекта '''

# заходим в новую папку нового проекта 
# в терминал вводим команду: python -m venv venv 
 
# далее активируем екзешник командой в терминале 
# venv\Scripts\activate

# в комвндной строке терминала в самом начале должна появится надпись (venv)

# скомпоновать библиотека в файл 
# pip freeze > requirements.txt

# распаковка файла с библиотеками
# pip install -r requirements.txt





'''Отправка проекта в репозиторий'''

# создать папку с именем '.git'

# инициализация гит
# git init

# добавление файлов в гит папку
# git add .
# git add filename.py.

# Сделайте первый коммит (фиксация изменений)
# git commit -m "Initial commit"

# Настройте удаленный репозиторий
# git remote add origin https://github.com/KaterinaGalisheva/Urban_FastAPI.git<URL-удаленного-репозитория>

# Отправьте изменения в удаленный репозиторий
# git push -u origin master

# Проверьте статус репозитория
# git status


