Тестовое задание.

Процедура запуска проекта:

1. $ git clone https://github.com/IlyaES1989/blog.git
2. $ cat > .env.dev
SECRET_KEY='значение SECRET_KEY'
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=admin@example.com
EMAIL_HOST_PASSWORD=password_from_email
DEFAULT_FROM_EMAIL=admin@example.com
DEBUG=True

3. $ docker build .
4. $ docker-compose run web python manage.py makemigrations nekidaem
5. $ docker-compose run web python manage.py migrate
6. $ docker-compose up -d
7. $ winpty docker-compose exec web python manage.py createsuperusen
8. $ docker-compose up

9. В браузере перейти по адресу 127.0.0.1/admin
10. Ввести Username и password ранее созданного superuser.
