run: #Команда для запуска локального сервера
	cd library/; \
	python manage.py runserver 8000

migrate: #Команда для миграции моделей
	cd library/; \
	python manage.py makemigrations
	cd library/; \
	python manage.py migrate

psql: #Вход в базу данных
	./runpsql.sh