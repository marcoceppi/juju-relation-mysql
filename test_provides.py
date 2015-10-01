import os
import unittest
from mock import patch, MagicMock

os.environ['CHARM_DIR'] = '/tmp'

from .provides import MySQL


class TestProvides(unittest.TestCase):
    def setUp(self):
        self.MySQL = MySQL('test')
        self.MySQL.conversation = MagicMock()

    def test_joined(self):
        self.MySQL.joined()
        self.MySQL.conversation.return_value.set_state.assert_called_with('{relation_name}.database.requested')

    def test_departed(self):
        self.MySQL.departed()
        self.MySQL.conversation.return_value.remove_state.assert_called_with('{relation_name}.database.requested')

    def test_requested_database(self):
        for d in self.MySQL.requested_databases():
            self.assertEqual(d, None)

    @patch('charms.reactive.decorators.get_states')
    def test_provide_database(self, m_states):
        m_states.side_effect = ['{provides:mysql}.database.requested']
        self.MySQL.provide_database('test', 'local', 3306, 't', 'u', 'p')
        self.MySQL.conversation.assert_called_with(scope='test')
        convo = self.MySQL.conversation.return_value
        convo.set_remote.assert_called_with(
            host='local',
            port=3306,
            database='t',
            user='u',
            password='p',
        )
        convo.set_local.assert_called_with('database', 't')
        convo.remove_state.assert_called_with('{relation_name}.database.requested')
