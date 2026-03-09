import pytest
from main_1_1 import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

# Уже существующие тесты...

def test_add_valid_books(collector):
    valid_names = ['Книга 1', 'Гарри Поттер', 'A' * 40, '123', 'К']
    for name in valid_names:
        collector.add_new_book(name)
        assert name in collector.books_genre

def test_add_invalid_length_books(collector):
    invalid_names = ['', 'A' * 41]
    for name in invalid_names:
        collector.add_new_book(name)
        assert name not in collector.books_genre

def test_add_duplicate_books(collector):
    collector.add_new_book('Книга')
    collector.add_new_book('Книга')
    assert list(collector.books_genre.keys()).count('Книга') == 1

def test_set_and_get_genre(collector):
    name = 'Книга'
    genre = 'Фантастика'
    collector.add_new_book(name)
    # Разделение операции: установка жанра
    collector.set_book_genre(name, genre)
    # Получение жанра
    assert collector.get_book_genre(name) == genre

def test_get_book_genre_default_empty(collector):
    name = 'Некоторая книга'
    collector.add_new_book(name)
    assert collector.get_book_genre(name) == ''

def test_books_for_children_excludes_adult(collector):
    collector.add_new_book('Приключение')
    collector.set_book_genre('Приключение', 'Фантастика')
    collector.add_new_book('Страшилка')
    collector.set_book_genre('Страшилка', 'Ужасы')

    books = collector.get_books_for_children()
    assert 'Приключение' in books
    assert 'Страшилка' not in books

def test_books_for_children_excludes_unset_genre(collector):
    collector.add_new_book('Это без жанра')
    assert 'Это без жанра' not in collector.get_books_for_children()

def test_get_all_books_dict(collector):
    collector.add_new_book('Книга1')
    collector.add_new_book('Книга2')
    assert 'Книга1' in collector.books_genre
    assert 'Книга2' in collector.books_genre

def test_get_books_by_genre(collector):
    collector.add_new_book('Книга1')
    collector.set_book_genre('Книга1', 'Фантастика')
    collector.add_new_book('Книга2')
    collector.set_book_genre('Книга2', 'Ужасы')

    genre = 'Фантастика'
    books = [name for name, g in collector.books_genre.items() if g == genre]
    assert 'Книга1' in books
    assert 'Книга2' not in books

# Новые тесты:

def test_get_books_with_specific_genre(collector):
    # Setup
    collector.add_new_book('Книга А')
    collector.set_book_genre('Книга А', 'Фантастика')
    collector.add_new_book('Книга Б')
    collector.set_book_genre('Книга Б', 'Драма')
    collector.add_new_book('Книга В')
    collector.set_book_genre('Книга В', 'Фантастика')

    # Тест
    fantasy_books = collector.get_books_with_specific_genre('Фантастика')
    assert 'Книга А' in fantasy_books
    assert 'Книга В' in fantasy_books
    assert 'Книга Б' not in fantasy_books

def test_get_books_genre_returns_current_dict(collector):
    # Setup
    collector.add_new_book('Книга1')
    collector.set_book_genre('Книга1', 'Жанр1')
    collector.add_new_book('Книга2')
    collector.set_book_genre('Книга2', 'Жанр2')

    genre_dict = collector.get_books_genre()
    assert isinstance(genre_dict, dict)
    assert genre_dict['Книга1'] == 'Жанр1'
    assert genre_dict['Книга2'] == 'Жанр2'

def test_add_and_delete_book_in_favorites(collector):
    # Добавляем книгу и добавляем в избранное
    name = 'Пушкин'
    collector.add_new_book(name)
    collector.add_book_in_favorites(name)
    favorites = collector.get_list_of_favorites_books()
    assert name in favorites

    # Удаляем из избранного
    collector.delete_book_from_favorites(name)
    favorites_after = collector.get_list_of_favorites_books()
    assert name not in favorites_after

def test_delete_nonexistent_book_from_favorites(collector):
    # Попытка удалить книгу, которой нет в избранных, не должна вызвать ошибку
    collector.delete_book_from_favorites('Некоторый不存在')
    # А список избранных не должен измениться
    assert collector.get_list_of_favorites_books() == []

# Проверка, что добавление книги в избранное работает корректно, даже если книга не в списке
def test_add_book_in_favorites_if_not_exists(collector):
    name = 'Несуществующая книга'
    # В этом случае, если метод позволяет, добавим вручную в избранное
    collector.add_book_in_favorites(name)
    favorites = collector.get_list_of_favorites_books()
    assert name in favorites