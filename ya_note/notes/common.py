from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note, User


class BaseNoteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Читатель простой')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='note-slug',
            author=cls.author
        )

# Common URLs
URL_HOME = reverse('notes:home')
URL_LIST = reverse('notes:list')
URL_ADD = reverse('notes:add')
URL_SUCCESS = reverse('notes:success')
URL_LOGIN = reverse('users:login')
URL_SIGNUP = reverse('users:signup')

def get_url_edit(note):
    return reverse('notes:edit', args=(note.slug,))

def get_url_detail(note):
    return reverse('notes:detail', args=(note.slug,))

def get_url_delete(note):
    return reverse('notes:delete', args=(note.slug,))
