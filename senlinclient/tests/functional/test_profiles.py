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

PROFILE_NAME = "PF001"


class ProfileTest(base.OpenStackClientTestBase):
    """Test for profiles"""

    def test_profile_list(self):
        result = self.openstack('cluster profile list')
        profile_list = self.parser.listing(result)
        self.assertTableStruct(profile_list, ['id', 'name', 'type',
                                              'created_at'])

    def test_pofile_create(self):
        result = self.profile_create(PROFILE_NAME)
        self.assertEqual(result['name'], PROFILE_NAME)
        self.addCleanup(self.profile_delete(result['id']))
