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

from senlinclient.tests.functional import base

POLICY_NAME = "PC001"


class PolicyTest(base.OpenStackClientTestBase):
    """Test for policies"""

    def test_policy_list(self):
        result = self.openstack('cluster policy list')
        policy_list = self.parser.listing(result)
        self.assertTableStruct(policy_list, ['id', 'name', 'type',
                                             'created_at'])

    def test_policy_create(self):
        result = self.policy_create(POLICY_NAME)
        self.assertEqual(result['name'], POLICY_NAME)
        self.addCleanup(self.policy_delete(result['id']))
