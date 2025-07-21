from http import HTTPStatus

from notes.tests.common import (URL_ADD, URL_HOME, URL_LIST, URL_LOGIN,
                                URL_SIGNUP, URL_SUCCESS, BaseNoteTestCase,
                                get_url_delete, get_url_detail, get_url_edit)


class TestRoutes(BaseNoteTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url_detail = get_url_detail(cls.note)
        cls.url_edit = get_url_edit(cls.note)
        cls.url_delete = get_url_delete(cls.note)

    def test_pages_availability(self):
        """Проверяем, что анонимному пользователю доступны страницы:
        главная страница, регистрации пользователей, входа в учётную запись.
        """
        urls = (URL_HOME, URL_LOGIN, URL_SIGNUP)
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note_edit_and_delete(self):
        """
        Проверяем, что страницы отдельной записи, редактирования записи
        и удаления записи доступна только автору заметки, другим
        пользователям при попытки зайти на данные страницы -
        вернётся ошибка 404.
        """
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.not_author_client, HTTPStatus.NOT_FOUND),
        )
        urls = (self.url_detail, self.url_edit, self.url_delete)
        for user, status in users_statuses:
            for url in urls:
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_pages_availability_for_auth_user(self):
        """
        Проверяем, что аутентифицированному пользователю
        доступны страницы: со списком заметок, успешного
        добавления заметки, добавления новой заметки.
        """
        urls = (URL_LIST, URL_SUCCESS, URL_ADD)
        for url in urls:
            with self.subTest(url=url):
                response = self.not_author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        """Проверяем, что при попытке перейти на страницы: списка заметок,
        успешного добавления записи, добавления заметки, отдельной заметки,
        редактирования или удаления заметки анонимный пользователь
        перенаправляется на страницу логина.
        """
        urls = (
            URL_LIST,
            self.url_edit,
            self.url_delete,
            URL_SUCCESS,
            URL_ADD,
            self.url_detail
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{URL_LOGIN}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
            self.url_delete,
            self.url_success,
            self.url_add,
            self.url_detail

        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.url_login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
