import pytest
from main import BooksCollector

@pytest.mark.parametrize('name', [
    'Книга 1',
    'Гарри Поттер',
    'A' * 40,
    '123',
    'К',
])
def test_add_valid_books_added(name):
    collector = BooksCollector()
    collector.add_new_book(name)
    assert name in collector.books_genre


@pytest.mark.parametrize('name', [
    '',
    'A' * 41,
])
def test_add_invalid_length_books_not_added(name):
    collector = BooksCollector()
    collector.add_new_book(name)
    assert name not in collector.books_genre


def test_add_duplicate_book_not_added_twice_case1():
    collector = BooksCollector()
    collector.add_new_book('Книга')
    collector.add_new_book('Книга')
    assert len(collector.books_genre) == 1


def test_add_duplicate_book_not_added_twice_case2():
    collector = BooksCollector()
    collector.add_new_book('Test')
    collector.add_new_book('Test')
    assert list(collector.books_genre.keys()) == ['Test']


def test_add_multiple_different_books():
    collector = BooksCollector()
    collector.add_new_book('Книга1')
    collector.add_new_book('Книга2')
    assert len(collector.books_genre) ==  2

@pytest.mark.parametrize('genre', [
    'Ужасы',
    'Детективы',
])
def test_age_rating_books_not_in_children_list(genre):
    collector = BooksCollector()
    collector.add_new_book('Книга')
    collector.set_book_genre('Книга', genre)

    assert 'Книга' not in collector.get_books_for_children()


@pytest.mark.parametrize('genre', [
    'Фантастика',
    'Мультфильмы',
    'Комедии',
])
def test_non_age_rating_books_in_children_list(genre):
    collector = BooksCollector()
    collector.add_new_book('Книга')
    collector.set_book_genre('Книга', genre)

    assert 'Книга' in collector.get_books_for_children()

def test_mixed_books_children_list_case1():
    collector = BooksCollector()
    collector.add_new_book('Ужастик')
    collector.add_new_book('Комедия')
    collector.set_book_genre('Ужастик', 'Ужасы')
    collector.set_book_genre('Комедия', 'Комедии')

    books = collector.get_books_for_children()
    assert 'Ужастик' not in books
    assert 'Комедия' in books

def test_mixed_books_children_list_case2():
    collector = BooksCollector()
    collector.add_new_book('Детектив')
    collector.add_new_book('Фантастика')
    collector.set_book_genre('Детектив', 'Детективы')
    collector.set_book_genre('Фантастика', 'Фантастика')
    
    books = collector.get_books_for_children()
    assert 'Детектив' not in books
    assert 'Фантастика' in books

def test_empty_genre_not_in_children_list():
    collector = BooksCollector()
    collector.add_new_book('Без жанра')
    assert 'Без жанра' not in collector.get_books_for_children()


def test_multiple_age_rating_books_not_returned():
    collector = BooksCollector()
    collector.add_new_book('Книга1')
    collector.add_new_book('Книга2')
    collector.set_book_genre('Книга1', 'Ужасы')
    collector.set_book_genre('Книга2', 'Детективы')

    assert collector.get_books_for_children() == []
 
    
@pytest.mark.parametrize('name', [
    'Книга1',
    'Гарри',
    'A' * 40,
    '12345',
    'TestBook',
])
def test_new_book_has_empty_genre(name):
    collector = BooksCollector()
    collector.add_new_book(name)
    assert collector.get_book_genre(name) == ''

def test_new_book_genre_is_empty_string():
    collector = BooksCollector()
    collector.add_new_book('Книга')
    assert collector.books_genre['Книга'] == ''

def test_multiple_new_books_have_no_genre():
    collector = BooksCollector()
    collector.add_new_book('Книга1')
    collector.add_new_book('Книга2')

    assert collector.get_book_genre('Книга1') == ''
    assert collector.get_book_genre('Книга2') == ''

def test_book_without_genre_not_in_children_list():
    collector = BooksCollector()
    collector.add_new_book('Книга')

    assert 'Книга' not in collector.get_books_for_children()

def test_genre_not_set_if_invalid():
    collector = BooksCollector()
    collector.add_new_book('Книга')
    collector.set_book_genre('Книга', 'Несуществующий жанр')

    assert collector.get_book_genre('Книга') == ''