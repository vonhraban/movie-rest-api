## Movies RESTful API

This project demonstrates the use of Django Rest Framework and Django ORM. 

### Running

`python3 movie_list/manage.py migrate`

`python3 movie_list/manage.py runserver`

This will run a HTTP server listening on port `8000`

http://127.0.0.1:8000/movies for master view

http://127.0.0.1:8000/movies/:id for detail view

### Testing
`python3 movie_list/manage.py test`
