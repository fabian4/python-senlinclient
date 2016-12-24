# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy

import mock
from openstack.cluster.v1 import receiver as sdk_receiver
from openstack import exceptions as sdk_exc
from osc_lib import exceptions as exc
import six

from senlinclient.common.i18n import _
from senlinclient.tests.unit.v1 import fakes
from senlinclient.v1 import receiver as osc_receiver


class TestReceiver(fakes.TestClusteringv1):
    def setUp(self):
        super(TestReceiver, self).setUp()
        self.mock_client = self.app.client_manager.clustering


class TestReceiverList(TestReceiver):
    columns = ['id', 'name', 'type', 'cluster_id', 'action', 'created_at']
    response = {"receivers": [
        {
            "action": "CLUSTER_SCALE_OUT",
            "actor": {
                "trust_id": [
                    "6dc6d336e3fc4c0a951b5698cd1236d9"
                ]
            },
            "channel": {
                "alarm_url": "http://node1:8778/v1/webhooks/e03dd2e5-8f2e-4ec1"
                             "-8c6a-74ba891e5422/trigger?V=1&count=1"
            },
            "cluster_id": "ae63a10b-4a90-452c-aef1-113a0b255ee3",
            "created_at": "2015-06-27T05:09:43",
            "domain": "Default",
            "id": "573aa1ba-bf45-49fd-907d-6b5d6e6adfd3",
            "name": "cluster_inflate",
            "params": {
                "count": "1"
            },
            "project": "6e18cc2bdbeb48a5b3cad2dc499f6804",
            "type": "webhook",
            "updated_at": 'null',
            "user": "b4ad2d6e18cc2b9c48049f6dbe8a5b3c"
        }
    ]}

    defaults = {
        'global_project': False,
        'marker': None,
        'limit': None,
        'sort': None,
    }

    def setUp(self):
        super(TestReceiverList, self).setUp()
        self.cmd = osc_receiver.ListReceiver(self.app, None)
        self.mock_client.receivers = mock.Mock(return_value=self.response)

    def test_receiver_list_defaults(self):
        arglist = []
        parsed_args = self.check_parser(self.cmd, arglist, [])
        columns, data = self.cmd.take_action(parsed_args)
        self.mock_client.receivers.assert_called_with(**self.defaults)
        self.assertEqual(self.columns, columns)

    def test_receiver_list_full_id(self):
        arglist = ['--full-id']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        columns, data = self.cmd.take_action(parsed_args)
        self.mock_client.receivers.assert_called_with(**self.defaults)
        self.assertEqual(self.columns, columns)

    def test_receiver_list_limit(self):
        kwargs = copy.deepcopy(self.defaults)
        kwargs['limit'] = '3'
        arglist = ['--limit', '3']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        columns, data = self.cmd.take_action(parsed_args)
        self.mock_client.receivers.assert_called_with(**kwargs)
        self.assertEqual(self.columns, columns)

    def test_receiver_list_sort(self):
        kwargs = copy.deepcopy(self.defaults)
        kwargs['sort'] = 'name:asc'
        arglist = ['--sort', 'name:asc']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        columns, data = self.cmd.take_action(parsed_args)
        self.mock_client.receivers.assert_called_with(**kwargs)
        self.assertEqual(self.columns, columns)

    def test_receiver_list_sort_invalid_key(self):
        self.mock_client.receivers = mock.Mock(
            return_value=self.response)
        kwargs = copy.deepcopy(self.defaults)
        kwargs['sort'] = 'bad_key'
        arglist = ['--sort', 'bad_key']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        self.mock_client.receivers.side_effect = sdk_exc.HttpException()
        self.assertRaises(sdk_exc.HttpException,
                          self.cmd.take_action, parsed_args)

    def test_receiver_list_sort_invalid_direction(self):
        self.mock_client.receivers = mock.Mock(
            return_value=self.response)
        kwargs = copy.deepcopy(self.defaults)
        kwargs['sort'] = 'name:bad_direction'
        arglist = ['--sort', 'name:bad_direction']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        self.mock_client.receivers.side_effect = sdk_exc.HttpException()
        self.assertRaises(sdk_exc.HttpException,
                          self.cmd.take_action, parsed_args)

    def test_receiver_list_filter(self):
        kwargs = copy.deepcopy(self.defaults)
        kwargs['name'] = 'my_receiver'
        arglist = ['--filter', 'name=my_receiver']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        columns, data = self.cmd.take_action(parsed_args)
        self.mock_client.receivers.assert_called_with(**kwargs)
        self.assertEqual(self.columns, columns)

    def test_receiver_list_marker(self):
        kwargs = copy.deepcopy(self.defaults)
        kwargs['marker'] = 'a9448bf6'
        arglist = ['--marker', 'a9448bf6']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        columns, data = self.cmd.take_action(parsed_args)
        self.mock_client.receivers.assert_called_with(**kwargs)
        self.assertEqual(self.columns, columns)


class TestReceiverShow(TestReceiver):
    get_response = {"receiver": {
        "action": "CLUSTER_SCALE_OUT",
        "actor": {
            "trust_id": [
                "6dc6d336e3fc4c0a951b5698cd1236d9"
            ]
        },
        "channel": {
            "alarm_url": "http://node1:8778/v1/webhooks/e03dd2e5-8f2e-4ec1-"
                         "8c6a-74ba891e5422/trigger?V=1&count=1"
        },
        "cluster_id": "ae63a10b-4a90-452c-aef1-113a0b255ee3",
        "created_at": "2015-06-27T05:09:43",
        "domain": "Default",
        "id": "573aa1ba-bf45-49fd-907d-6b5d6e6adfd3",
        "name": "cluster_inflate",
        "params": {
            "count": "1"
        },
        "project": "6e18cc2bdbeb48a5b3cad2dc499f6804",
        "type": "webhook",
        "updated_at": 'null',
        "user": "b4ad2d6e18cc2b9c48049f6dbe8a5b3c"
    }}

    def setUp(self):
        super(TestReceiverShow, self).setUp()
        self.cmd = osc_receiver.ShowReceiver(self.app, None)
        x_receiver = sdk_receiver.Receiver(**self.get_response['receiver'])
        self.mock_client.get_receiver = mock.Mock(return_value=x_receiver)

    def test_receiver_show(self):
        arglist = ['my_receiver']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        self.cmd.take_action(parsed_args)
        self.mock_client.get_receiver.assert_called_with('my_receiver')

    def test_receiver_show_not_found(self):
        arglist = ['my_receiver']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        self.mock_client.get_receiver.side_effect = sdk_exc.ResourceNotFound()
        error = self.assertRaises(exc.CommandError, self.cmd.take_action,
                                  parsed_args)
        self.assertEqual('Receiver not found: my_receiver', str(error))


class TestReceiverCreate(TestReceiver):
    response = {"receiver": {
        "action": "CLUSTER_SCALE_OUT",
        "actor": {
            "trust_id": [
                "6dc6d336e3fc4c0a951b5698cd1236d9"
            ]
        },
        "channel": {
            "alarm_url": "http://node1:8778/v1/webhooks/e03dd2e5-8f2e-4ec"
                         "1-8c6a-74ba891e5422/trigger?V=1&count=1"
        },
        "cluster_id": "ae63a10b-4a90-452c-aef1-113a0b255ee3",
        "created_at": "2015-06-27T05:09:43",
        "domain": "Default",
        "id": "573aa1ba-bf45-49fd-907d-6b5d6e6adfd3",
        "name": "cluster_inflate",
        "params": {
            "count": "1"
        },
        "project": "6e18cc2bdbeb48a5b3cad2dc499f6804",
        "type": "webhook",
        "updated_at": 'null',
        "user": "b4ad2d6e18cc2b9c48049f6dbe8a5b3c"
    }}

    args = {
        "action": "CLUSTER_SCALE_OUT",
        "cluster_id": "my_cluster",
        "name": "my_receiver",
        "params": {
            "count": "1"
        },
        "type": "webhook"
    }

    def setUp(self):
        super(TestReceiverCreate, self).setUp()
        self.cmd = osc_receiver.CreateReceiver(self.app, None)
        self.mock_client.create_receiver = mock.Mock(
            return_value=sdk_receiver.Receiver(**self.response['receiver']))
        self.mock_client.get_receiver = mock.Mock(
            return_value=sdk_receiver.Receiver(**self.response['receiver']))

    def test_receiver_create_webhook(self):
        arglist = ['my_receiver', '--action', 'CLUSTER_SCALE_OUT',
                   '--cluster', 'my_cluster', '--params', 'count=1',
                   '--type', 'webhook']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        self.cmd.take_action(parsed_args)
        self.mock_client.create_receiver.assert_called_with(**self.args)

    def test_receiver_create_webhook_failed(self):
        arglist = ['my_receiver', '--action', 'CLUSTER_SCALE_OUT',
                   '--params', 'count=1', '--type', 'webhook']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        error = self.assertRaises(exc.CommandError, self.cmd.take_action,
                                  parsed_args)
        self.assertIn(_('cluster and action parameters are required to create '
                        'webhook type of receiver'), str(error))

    def test_receiver_create_non_webhook(self):
        arglist = ['my_receiver', '--params', 'count=1',
                   '--type', 'foo']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        self.cmd.take_action(parsed_args)
        args = copy.deepcopy(self.args)
        args['type'] = 'foo'
        args['cluster_id'] = None
        args['action'] = None
        self.mock_client.create_receiver.assert_called_with(**args)


class TestReceiverDelete(TestReceiver):
    def setUp(self):
        super(TestReceiverDelete, self).setUp()
        self.cmd = osc_receiver.DeleteReceiver(self.app, None)
        self.mock_client.delete_receiver = mock.Mock()

    def test_receiver_delete(self):
        arglist = ['receiver1', 'receiver2', 'receiver3']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        self.cmd.take_action(parsed_args)
        self.mock_client.delete_receiver.assert_has_calls(
            [mock.call('receiver1', False), mock.call('receiver2', False),
             mock.call('receiver3', False)]
        )

    def test_receiver_delete_force(self):
        arglist = ['receiver1', 'receiver2', 'receiver3', '--force']
        parsed_args = self.check_parser(self.cmd, arglist, [])
        self.cmd.take_action(parsed_args)
        self.mock_client.delete_receiver.assert_has_calls(
            [mock.call('receiver1', False), mock.call('receiver2', False),
             mock.call('receiver3', False)]
        )

    def test_receiver_delete_not_found(self):
        arglist = ['my_receiver']
        self.mock_client.delete_receiver.side_effect = (
            sdk_exc.ResourceNotFound)
        parsed_args = self.check_parser(self.cmd, arglist, [])
        error = self.assertRaises(exc.CommandError, self.cmd.take_action,
                                  parsed_args)
        self.assertIn('Failed to delete 1 of the 1 specified receiver(s).',
                      str(error))

    def test_receiver_delete_one_found_one_not_found(self):
        arglist = ['receiver1', 'receiver2']
        self.mock_client.delete_receiver.side_effect = (
            [None, sdk_exc.ResourceNotFound]
        )
        parsed_args = self.check_parser(self.cmd, arglist, [])
        error = self.assertRaises(exc.CommandError,
                                  self.cmd.take_action, parsed_args)
        self.mock_client.delete_receiver.assert_has_calls(
            [mock.call('receiver1', False), mock.call('receiver2', False)]
        )
        self.assertEqual('Failed to delete 1 of the 2 specified receiver(s).',
                         str(error))

    @mock.patch('sys.stdin', spec=six.StringIO)
    def test_receiver_delete_prompt_yes(self, mock_stdin):
        arglist = ['my_receiver']
        mock_stdin.isatty.return_value = True
        mock_stdin.readline.return_value = 'y'
        parsed_args = self.check_parser(self.cmd, arglist, [])

        self.cmd.take_action(parsed_args)

        mock_stdin.readline.assert_called_with()
        self.mock_client.delete_receiver.assert_called_with('my_receiver',
                                                            False)

    @mock.patch('sys.stdin', spec=six.StringIO)
    def test_receiver_delete_prompt_no(self, mock_stdin):
        arglist = ['my_receiver']
        mock_stdin.isatty.return_value = True
        mock_stdin.readline.return_value = 'n'
        parsed_args = self.check_parser(self.cmd, arglist, [])

        self.cmd.take_action(parsed_args)

        mock_stdin.readline.assert_called_with()
        self.mock_client.delete_receiver.assert_not_called()
