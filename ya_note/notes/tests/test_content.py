from notes.forms import NoteForm
from notes.models import Note
from notes.tests.common import (URL_ADD, URL_LIST, BaseNoteTestCase,
                                get_url_edit)


class TestContent(BaseNoteTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url_edit = get_url_edit(cls.note)

    def test_notes_list_for_different_users(self):
        """
        Проверяем, что отдельная заметка передаётся на страницу
        со списком заметок и что, в список заметок одного
        пользователя не попадают заметки другого пользователя.
        """
        users_result = (
            (self.author_client, True),
            (self.not_author_client, False),
        )
        for user, result in users_result:
            with self.subTest(user=user):
                response = user.get(URL_LIST)
                object_list = response.context['object_list']
                assert (self.note in object_list) is result

    def test_pages_contains_form(self):
        """
        Проверяем, что на страницы создания и редактирования
        заметки передаются формы.
        """
        urls = (self.url_edit, URL_ADD)
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                assert 'form' in response.context
                assert isinstance(response.context['form'], NoteForm)
