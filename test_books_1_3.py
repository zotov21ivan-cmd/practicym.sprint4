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

def test_set_book_genre_assigned_value(collector):
    name = 'Книга'
    genre = 'Фантастика'
    collector.add_new_book(name)
    collector.set_book_genre(name, genre)
    assert collector.get_book_genre(name) == genre

def test_get_book_genre_default_empty(collector):
    name = 'Некоторая книга'
    collector.add_new_book(name)
    # Без установки жанра по умолчанию возвращается ''
    assert collector.get_book_genre(name) == ''

# Тесты для получения книг для детей по жанру

def test_get_books_for_children_includes_adventure(collector):
    name = 'Приключение'
    genre = 'Фантастика'
    collector.add_new_book(name)
    collector.set_book_genre(name, genre)
    # Проверка, что книга для детей включена
    assert name in collector.get_books_for_children()

def test_get_books_for_children_excludes_horror(collector):
    name = 'Страшилка'
    genre = 'Ужасы'
    collector.add_new_book(name)
    collector.set_book_genre(name, genre)
    # Проверка, что книга ужасов исключена
    books = collector.get_books_for_children()
    assert name not in books

def test_get_books_for_children_excludes_unset_genre(collector):
    name = 'Это без жанра'
    collector.add_new_book(name)
    # Книга без жанра не должна включаться
    assert name not in collector.get_books_for_children()

# Тест на получение полного словаря книг и жанров

def test_get_books_genre_returns_current_dict(collector):
    name1 = 'Книга1'
    name2 = 'Книга2'
    genre1 = 'Жанр1'
    genre2 = 'Жанр2'
    collector.add_new_book(name1)
    collector.set_book_genre(name1, genre1)
    collector.add_new_book(name2)
    collector.set_book_genre(name2, genre2)
    genre_dict = collector.get_books_genre()
    assert genre_dict[name1] == genre1
    assert genre_dict[name2] == genre2

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