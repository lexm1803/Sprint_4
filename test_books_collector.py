import pytest

import test_data

class TestAddNewBook:

    @pytest.mark.parametrize('name_book', test_data.VALID_BOOK_NAMES)
    def test_add_new_book_valid_name(self, collector, name_book):
        collector.add_new_book(name_book)
        assert name_book in collector.books_genre
        assert collector.books_genre[name_book] == ''

    @pytest.mark.parametrize('name_book', test_data.INVALID_BOOK_NAMES)
    def test_add_new_book_invalid_name(self, collector, name_book):
        collector.add_new_book(name_book)
        assert name_book not in collector.books_genre
        
    def test_add_new_book_dublicate(self, collector):
         collector.add_new_book("Мертвые души")
         collector.add_new_book("Мертвые души")
         assert list(collector.books_genre.keys()).count("Мертвые души") == 1

class TestSetBookGenre:

    def test_set_book_valid_genre(self, collector):
        collector.add_new_book("Марсианские хроники")
        collector.set_book_genre("Марсианские хроники", "Фантастика")
        assert collector.get_book_genre("Марсианские хроники") == "Фантастика"

    @pytest.mark.parametrize('genre', test_data.INVALID_GENRES)
    def test_set_book_invalid_genre(self, collector, genre):
        collector.add_new_book("Гордость и предубеждение")
        collector.set_book_genre("Гордость и предубеждение", genre)
        assert collector.get_book_genre("Гордость и предубеждение") == ""

    def test_set_book_genre_none_existing_book(self, collector):
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert "Несуществующая книга" not in collector.books_genre

class TestGetBooksWithSpecificGenre:

    @pytest.mark.parametrize('genre', test_data.VALID_GENRES)
    def test_get_books_with_specific_valid_genre(self, fill_collector, genre):
        result = fill_collector.get_books_with_specific_genre(genre)
        assert isinstance(result, list)
        
        for book in result:
            assert fill_collector.books_genre[book] == genre
    
    @pytest.mark.parametrize('genre', test_data.INVALID_GENRES)
    def test_get_books_with_specific_invalid_genre(self, collector, genre):
        result = collector.get_books_with_specific_genre(genre)
        assert result == []

class TestGetBooksForChildren:

    def test_get_books_for_children(self, fill_collector):
        children_books = fill_collector.get_books_for_children()
        
        assert isinstance(children_books, list)
        
        for book in test_data.CHILDREN_BOOKS:
            assert book in children_books
        
        for book in test_data.ADULT_BOOKS:
            assert book not in children_books

        assert "Без жанра" not in children_books

class TestAddBookInFavorites:

    def test_add_book_in_favorites(self, collector):
        collector.add_new_book("Хозяйка Медной горы")
        collector.add_book_in_favorites("Хозяйка Медной горы")
        assert "Хозяйка Медной горы" in collector.favorites

    def test_add_none_existing_book_in_favorites_ignored(self, collector):
        collector.add_book_in_favorites("Несуществующая книга")
        assert "Несуществующая книга" not in collector.favorites

    def test_add_book_in_favorites_double(self, collector):
        collector.add_new_book("Дубль")
        collector.add_book_in_favorites("Дубль")
        collector.add_book_in_favorites("Дубль")
        assert collector.favorites.count("Дубль") == 1

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Оно")
        collector.add_book_in_favorites("Оно")
        collector.delete_book_from_favorites("Оно")
        assert "Оно" not in collector.favorites
    
    def test_delete_non_favorites_not_error(self, collector):
        collector.add_new_book("Смешарики")
        collector.delete_book_from_favorites("Смешарики")
        assert "Смешарики" not in collector.favorites    

    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Звездные войны")
        collector.add_book_in_favorites("Звездные войны")
        list_of_favorites_books = collector.get_list_of_favorites_books()
        assert list_of_favorites_books == ["Звездные войны"]

class TestGetBooksGenre:
    
    def test_get_books_genre(self, collector):
        collector.add_new_book("Пеппа")
        list_of_books = collector.get_books_genre()
        assert isinstance(list_of_books, dict)
        assert list_of_books == {"Пеппа": ""}

    def test_get_books_genre_with_a_genre(self, collector):
        collector.add_new_book("Кот из Ада")
        collector.set_book_genre("Кот из Ада", "Ужасы")
        assert collector.get_book_genre("Кот из Ада") == "Ужасы"

    def test_get_books_genre_non_exist(sel, collector):
        assert collector.get_book_genre("Несуществующая книга") is None