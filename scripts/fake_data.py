import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_market.settings')
from pprint import pprint
import requests

from books.api.serializers import BookSerializer


import django
django.setup()

from django.contrib.auth.models import User

from faker import Faker

def set_user(fakegen=None):
    if fakegen is None:
        fakegen = Faker(['en_US'])

    f_name = fakegen.first_name()
    l_name = fakegen.last_name()
    u_name = f_name.lower() + '_' + l_name.lower()
    email = f'{u_name}@{fakegen.domain_name()}'

    user_check = User.objects.filter(username=u_name)

    while user_check.exists():
        print(f'User is already created : {u_name}')
        u_name = f_name + '_' + l_name + str(random.randrange(1, 999))
        user_check = User.objects.filter(username=u_name)


    user = User(
        username =  u_name,
        first_name =  f_name,
        last_name = l_name,
        email =  email,
    )

    user.set_password('testing123')
    user.save()

    user_check = User.objects.filter(username=u_name)[0]
    print(f'User registered {user_check.username}, {user_check.id} with id number.')

def book_append(topic):
    fake = Faker(['en_US'])
    url = 'http://openlibrary.org/search.json'
    payload = {'q': topic}
    response = requests.get(url, params=payload)
 
    if response.status_code != 200:
        print('Incorrect request made', response.status_code)
        return

    jsn = response.json()
    books = jsn.get('docs')

    for book in books:
        book_name = book.get('title')
        data = dict(
            name = book_name,
            writer = book.get('author_name')[0],
            description = book.get('author_name')[0],
            published_at = fake.date_time_between(start_date='-10y', end_date='now', tzinfo=None),
        )

        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print('Book saved: ', book_name)
        else:
            continue