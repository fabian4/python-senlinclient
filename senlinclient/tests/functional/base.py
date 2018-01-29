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

import os
import six

from tempest.lib.cli import base
from tempest.lib.cli import output_parser


class OpenStackClientTestBase(base.ClientTestBase):
    """Command line client base functions."""

    def setUp(self):
        super(OpenStackClientTestBase, self).setUp()
        self.parser = output_parser

    def _get_clients(self):
        cli_dir = os.environ.get(
            'OS_SENLINCLIENT_EXEC_DIR',
            os.path.join(os.path.abspath('.'), '.tox/functional/bin'))

        return base.CLIClient(
            username=os.environ.get('OS_USERNAME'),
            password=os.environ.get('OS_PASSWORD'),
            tenant_name=os.environ.get('OS_TENANT_NAME'),
            uri=os.environ.get('OS_AUTH_URL'),
            cli_dir=cli_dir)

    def openstack(self, *args, **kwargs):
        return self.clients.openstack(*args, **kwargs)

    def _show_to_dict(self, output):
        obj = {}
        items = self.parser.listing(output)
        for item in items:
            obj[item['Field']] = six.text_type(item['Value'])
        return dict((self._key_name(k), v) for k, v in obj.items())

    def _key_name(self, key):
        return key.lower().replace(' ', '_')

    def _get_profile_path(self, profile_name):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'profiles/nova_server/%s' % profile_name)

    def _get_policy_path(self, policy_name):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'policies/%s' % policy_name)

    def policy_create(self, name):
        pf = self._get_policy_path('deletion_policy.yaml')
        cmd = ('cluster policy create --spec-file %s %s'
               % (pf, name))
        policy_raw = self.openstack(cmd)
        result = self._show_to_dict(policy_raw)
        return result

    def policy_delete(self, id):
        cmd = ('cluster policy delete %s --force' % id)
        self.openstack(cmd)

    def profile_create(self, name):
        pf = self._get_profile_path('cirros_basic.yaml')
        cmd = ('cluster profile create --spec-file %s %s'
               % (pf, name))
        profile_raw = self.openstack(cmd)
        result = self._show_to_dict(profile_raw)
        return result

    def profile_delete(self, id):
        cmd = ('cluster profile delete %s --force' % id)
        self.openstack(cmd)
