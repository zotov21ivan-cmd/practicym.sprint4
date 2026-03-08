import pytest
from main_1_1 import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

def test_add_valid_books(collector):    # Проверка добавления корректных книг
    valid_names = ['Книга 1', 'Гарри Поттер', 'A' * 40, '123', 'К']
    for name in valid_names:
        collector.add_new_book(name)
        assert name in collector.books_genre

def test_add_invalid_length_books(collector):       # Проверка на недопустимую длину

    invalid_names = ['', 'A' * 41]
    for name in invalid_names:
        collector.add_new_book(name)
        assert name not in collector.books_genre

def test_add_duplicate_books(collector):     # Проверка исключения проверок

    collector.add_new_book('Книга')
    collector.add_new_book('Книга')
    assert list(collector.books_genre.keys()).count('Книга') == 1

def test_set_and_get_genre(collector):    # Проверка установки и получения жанра
  
    name = 'Книга'
    genre = 'Фантастика'
    collector.add_new_book(name)
    collector.set_book_genre(name, genre)
    assert collector.get_book_genre(name) == genre

def test_get_book_genre_default_empty(collector):     # Проверка, если жанр не задан

    name = 'Некоторая книга'
    collector.add_new_book(name)
    assert collector.get_book_genre(name) == ''

def test_books_for_children_excludes_adult(collector):     # Проверка фильтрации книг для детей по жанрам

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

def test_get_all_books_dict(collector):     # Проверка получения полного списка книг

    collector.add_new_book('Книга1')
    collector.add_new_book('Книга2')
    assert 'Книга1' in collector.books_genre
    assert 'Книга2' in collector.books_genre

def test_get_books_by_genre(collector):     # Проверка получения книг по жанру

    collector.add_new_book('Книга1')
    collector.set_book_genre('Книга1', 'Фантастика')
    collector.add_new_book('Книга2')
    collector.set_book_genre('Книга2', 'Ужасы')


    genre = 'Фантастика'                            # фильтр по жанру
    books = [name for name, g in collector.books_genre.items() if g == genre]
    assert 'Книга1' in books
    assert 'Книга2' not in books
    
    
    
    #итого мне было проще почти все преписать, я сделал тесты на тему 
    #установка и полчение жанра, получение всего словаря книг, получение книг по жанру
    # проверку длинны названия книги, добавление книги и фильтрация в детский список