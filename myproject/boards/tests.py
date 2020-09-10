from django.test import TestCase
# from django.core.urlresolvers import reverse - deprecated and removed in Django 2.0
from django.urls import reverse, resolve

from boards.views import boards, board_topics, new_topic
from boards.models import Board


class BoardsTests(TestCase):

	def setUp(self):
		self.board = Board.objects.create(name='Django', description='Django board..')
		url = reverse('boards')
		self.response = self.client.get(url)
	
	def test_boards_view_status_code(self):				
		self.assertEquals(self.response.status_code, 200)

	def test_boards_url_resolves_boards_view(self):
		view = resolve('/boards/')
		self.assertEquals(view.func, boards)

	def test_boards_view_contains_link_to_topics_page(self):
		board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
		self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):

	def setUp(self):
		Board.objects.create(name='Django', description='Django board..')

	def test_board_topics_view_success_status_code(self):
		url = reverse('board_topics', kwargs={'pk': 1})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_board_topics_view_not_found_status_code(self):
		url = reverse('board_topics', kwargs={'pk': 99})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_board_topics_url_reolves_board_topics_view(self):
		view = resolve('/boards/1/')
		self.assertEquals(view.func, board_topics)

	def test_board_topics_view_contains_navigation_links(self):
		board_topics_url = reverse('board_topics', kwargs={'pk': 1})
		response = self.client.get(board_topics_url)
		boardspage_url = reverse('boards')
		new_topic_url = reverse('new_topic', kwargs={'pk': 1})
		self.assertContains(response, 'href="{0}"'.format(boardspage_url))
		self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicTests(TestCase):

	def setUp(self):
		Board.objects.create(name='Django', description='Django board..')

	def test_new_topic_view_success_status_code(self):
		url = reverse('new_topic', kwargs={'pk': 1})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_new_topic_view_not_found_status_code(self):
		url = reverse('new_topic', kwargs={'pk': 99})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_new_topic_url_resolves_new_topic_view(self):
		view = resolve('/boards/1/new/')
		self.assertEquals(view.func, new_topic)

	def test_new_topic_view_contains_link_back_to_board_topics_view(self):
		new_topic_url = reverse('new_topic', kwargs={'pk': 1})
		board_topics_url = reverse('board_topics', kwargs={'pk': 1})
		response = self.client.get(new_topic_url)
		self.assertContains(response, 'href="{0}'.format(board_topics_url))
