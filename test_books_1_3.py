import pytest
from main_1_2 import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

# Тесты, проверяющие добавление новых книг

def test_add_new_book_valid_name(collector):
    name = 'Гарри Поттер'
    collector.add_new_book(name)
    assert name in collector.books_genre

def test_add_new_book_empty_name(collector):
    name = ''
    collector.add_new_book(name)
    assert name not in collector.books_genre

def test_add_new_book_too_long_name(collector):
    name = 'A' * 41
    collector.add_new_book(name)
    assert name not in collector.books_genre
    
def test_add_new_book_duplicate_name(collector):
    name = 'Книга'
    collector.add_new_book(name)
    collector.add_new_book(name)
    # Проверка, что книга добавлена только один раз
    assert list(collector.books_genre.keys()).count(name) == 1

# Тесты для установки и получения жанра

def test_get_book_genre_direct_dict_access(collector):
    name = 'Некоторая книга'
    genre = 'Детская литература'
    collector.books_genre[name] = {'genre': genre} 
    # Проверяем, что get_book_genre возвращает правильное значение
    assert collector.get_book_genre(name) == genre

def test_set_book_genre_direct_verification(collector):
    name = 'Книга для проверки'
    genre = 'Фантастика'
    # Вызываем метод установки жанра
    collector.set_book_genre(name, genre)
    # Проверяем напрямую, что жанр записался в внутренний словарь
    assert collector.books_genre[name]['genre'] == genre

# Тесты для получения книг для детей по жанру
def test_get_books_for_children_returns_only_relevant_books(collector):
    # Создаём книги с разными жанрами
    adventure_name = 'Приключение'
    horror_name = 'Страшилка'
    no_genre_name = 'Без жанра'

    # Добавляем книги
    collector.add_new_book(adventure_name)
    collector.set_book_genre(adventure_name, 'Фантастика')

    collector.add_new_book(horror_name)
    collector.set_book_genre(horror_name, 'Ужасы')

    collector.add_new_book(no_genre_name)

    # Получаем список книг для детей
    books_for_children = collector.get_books_for_children()
    
    # Проверяем, что книга "Приключение" включена
    assert adventure_name in books_for_children, "Книга 'Приключение' должна быть в списке."
    # Проверяем, что книга "Страшилка" исключена
    assert horror_name not in books_for_children, "Книга 'Страшилка' не должна быть в списке."
    # Проверяем, что книга без жанра исключена
    assert no_genre_name not in books_for_children, "Книга без жанра не должна быть в списке."
    
# Тест на получение книг по конкретному жанру

def test_get_books_with_specific_genre_fantasy(collector):
    collector.add_new_book('Книга А')
    collector.set_book_genre('Книга А', 'Фантастика')
    collector.add_new_book('Книга Б')
    collector.set_book_genre('Книга Б', 'Драма')
    collector.add_new_book('Книга В')
    collector.set_book_genre('Книга В', 'Фантастика')
    fantasy_books = collector.get_books_with_specific_genre('Фантастика')
    assert 'Книга А' in fantasy_books
    assert 'Книга В' in fantasy_books
    assert 'Книга Б' not in fantasy_books

# Тест на возврат текущего словаря жанровых книг

def test_get_books_genre_returns_current_dict(collector):
    collector.add_new_book('Книга1')
    collector.set_book_genre('Книга1', 'Жанр1')
    collector.add_new_book('Книга2')
    collector.set_book_genre('Книга2', 'Жанр2')
    genre_dict = collector.get_books_genre()
    assert genre_dict == {
        'Книга1': 'Жанр1',
        'Книга2': 'Жанр2'
    }

# Тесты для работы с избранным

def check_favorites_list(collector, expected_list):
    # Получаем текущий список избранных книг
    favorites = collector.get_list_of_favorites_books()
    # Проверяем, что список совпадает с ожидаемым
    assert sorted(favorites) == sorted(expected_list)

def test_add_book_in_favorites_success(collector):
    name = 'Пушкин'
    collector.add_new_book(name)
    collector.add_book_in_favorites(name)
    favorites = collector.get_list_of_favorites_books()
    assert name in favorites

def test_delete_book_from_favorites_removes(collector):
    name = 'Пушкин'
    collector.add_new_book(name)
    collector.add_book_in_favorites(name)
    collector.delete_book_from_favorites(name)
    favorites = collector.get_list_of_favorites_books()
    assert name not in favorites

def test_delete_nonexistent_book_from_favorites(collector):
    # Удаление несуществующей книги с избранных не вызывает ошибок
    collector.delete_book_from_favorites('Некоторая отсутствующая книга')
    # Список избранных не должен измениться и оставаться пустым
    assert collector.get_list_of_favorites_books() == []

def test_add_book_in_favorites_if_not_exists(collector):
    name = 'Несуществующая книга'
    # Попытка добавить в избранное человека, которого нет в списке
    collector.add_book_in_favorites(name)
    favorites = collector.get_list_of_favorites_books()
    assert name in favorites