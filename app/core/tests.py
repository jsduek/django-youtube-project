# docker-compose run --rm app sh -c 'python manage.py test core'

from django.test import SimpleTestCase
from django.core.management import call_command
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OperationalError
from unittest.mock import patch # 중간에 가로채는 기능

#db연결 시도를 가로챔
@patch('django.db.utils.ConnectionHandler.__getitem__')
class CommendsTests(SimpleTestCase):
	# DB가 준비되었을 때 wait_for_db가 잘 동작하는 지 체크하는 함수
	def test_wait_for_db_ready(self, patched_getitem):
		patched_getitem.return_value = True

		call_command('wait_for_db')

		self.assertEqual(patched_getitem.call_count, 1)
		
	# DB연결에 오류가 발생했다고 가정을 하고 테스트
	@patch('time.sleep')
	def test_wait_for_db_delay(self, patched_sleep, patched_getitem):
		# Psycopg2에러 1번 OperationalError 5번 후 True
		patched_getitem.side_effect = [Psycopg2OperationalError] + \
			[OperationalError] * 5 + [True]

		call_command('wait_for_db')

		self.assertEqual(patched_getitem.call_count, 7)