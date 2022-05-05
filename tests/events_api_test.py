from constants import *
from requests import get, post, put, delete
from pprint import pprint


if LOCAL_MODE:
    app_address = f"http://{LOCAL_HOST}:{LOCAL_PORT}"
else:
    app_address = PROJECT_URL

print()
print(f'Адрес сайта: {app_address}')

# Получение списка всех мероприятий
print()
print('Получение списка всех мероприятий:')
pprint(get(app_address + '/api/events').json())

# Ошибочный запрос на получение одного мероприятия — неверный id
print()
print('Ошибочный запрос на получение одного мероприятия - неверный id:')
pprint(get(app_address + '/api/events/999').json())

# Ошибочный запрос на получение одного мероприятия — строка
print()
print('Ошибочный запрос на получение одного мероприятия - строка:')
pprint(get(app_address + '/api/events/abc').json())

# Корректный запрос на добавление мероприятия:
print()
print('Корректный запрос на добавление мероприятия:')
print(post(app_address + '/api/events',
           json={
               'title': 'Тестовое',
               'manager_id': 3,
               'is_private': False,
               'is_done': False,
           }).json())

# Получение списка всех мероприятий
print()
print('Получение списка всех мероприятий:')
req_dict = get(app_address + '/api/events').json() 
pprint(req_dict)

new_event_id = len(req_dict['events'])

# Некорректный запрос на добавление мероприятия - параметр json не указан:
print()
print('Некорректный запрос на добавление мероприятия - параметр json не указан:')
print(post(app_address + '/api/events').json())

# Некорректный запрос на добавление мероприятия - отсутствуют необходимые параметры:
print()
print('Некорректный запрос на добавление мероприятия - отсутствуют необходимые параметры:')
print(post(app_address + '/api/events',
           json={
               'title': 'Тестовое',
               'manager_id': 2,
           }).json())

# Корректный запрос на изменение данных мероприятия
print()
print('Корректный запрос на изменение данных мероприятия:')
print(put(app_address + f'/api/events/{new_event_id}',
          json={
              'title': 'Тестовое(изменённое)',
              'manager_id': 3,
              'is_private': False,
              'is_done': False,
          }).json())

# Корректное получение одного мероприятия
print()
print('Корректное получение одного мероприятия:')
pprint(get(app_address + f'/api/events/{new_event_id}').json())

# Корректный запрос на изменение данных мероприятия
print()
print('Некорректный запрос на изменение данных мероприятия - отсутствуют необходимые параметры:')
print(put(app_address + f'/api/events/{new_event_id}',
          json={
              'manager_id': 4,
              'is_private': True,
              'is_done': False,
          }).json())

# Корректный запрос на удаление мероприятия:
print()
print('Корректный запрос на удаление мероприятия:')
print(delete(app_address + f'/api/events/{new_event_id}').json())

# Получение всех мероприятий
print()
print('Получение всех мероприятий:')
pprint(get(app_address + '/api/events').json())

# Некорректный запрос на удаление мероприятия - пользователь с таким id не существует:
print()
print('Некорректный запрос на удаление мероприятия - пользователь с таким id не существует:')
print(delete(app_address + '/api/events/999').json())

# Некорректный запрос на удаление мероприятия - строка вмеcто id:
print()
print('Некорректный запрос на удаление мероприятия - строка вмеcто id:')
pprint(get(app_address + '/api/events/abc').json())
