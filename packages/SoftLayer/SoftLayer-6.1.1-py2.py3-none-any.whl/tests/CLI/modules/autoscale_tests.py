"""
    SoftLayer.tests.CLI.modules.autoscale_tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT, see LICENSE for more details.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for the autoscale cli command
"""

import sys
from unittest import mock as mock

from SoftLayer import fixtures
from SoftLayer import testing

import tempfile


class AutoscaleTests(testing.TestCase):

    def test_logs_dates(self):
        result = self.run_command(['autoscale', 'logs', '123456', '-d', '2019-02-02'])
        print(result)
        self.assert_no_fail(result)

    def test_scale_down(self):
        result = self.run_command(['autoscale', 'scale', '123456', '--down', '--by', '--amount', '2'])
        self.assert_no_fail(result)

    def test_scale_up(self):
        result = self.run_command(['autoscale', 'scale', '123456', '--up', '--to', '--amount', '2'])
        self.assert_no_fail(result)

    def test_scale_to(self):
        result = self.run_command(['autoscale', 'scale', '789654123', '--down', '--to', '--amount', '2'])
        self.assert_no_fail(result)

    def test_scale_by_up(self):
        result = self.run_command(['autoscale', 'scale', '789654123', '--by', '--down', '--amount', '-1'])
        self.assert_no_fail(result)

    def test_scale_cancel(self):
        result = self.run_command(['autoscale', 'scale', '789654123', '--by', '--down', '--amount', '1'])
        self.assert_no_fail(result)

    def test_autoscale_list(self):
        result = self.run_command(['autoscale', 'list'])
        self.assert_no_fail(result)

    def test_autoscale_detail(self):
        result = self.run_command(['autoscale', 'detail', '12222222'])
        self.assert_no_fail(result)

    def test_autoscale_tag(self):
        result = self.run_command(['autoscale', 'tag', '12345'])
        self.assert_no_fail(result)

    @mock.patch('SoftLayer.managers.autoscale.AutoScaleManager.edit')
    def test_autoscale_edit(self, manager):
        result = self.run_command(['autoscale', 'edit', '12345', '--name', 'test'])
        self.assert_no_fail(result)
        manager.assert_called_with('12345', {'name': 'test'})

    @mock.patch('SoftLayer.managers.autoscale.AutoScaleManager.edit')
    def test_autoscale_edit_userdata(self, manager):
        group = fixtures.SoftLayer_Scale_Group.getObject
        template = {
            'virtualGuestMemberTemplate': group['virtualGuestMemberTemplate']
        }
        template['virtualGuestMemberTemplate']['userData'] = [{'value': 'test'}]

        result = self.run_command(['autoscale', 'edit', '12345', '--userdata', 'test'])
        self.assert_no_fail(result)
        manager.assert_called_with('12345', template)

    @mock.patch('SoftLayer.managers.autoscale.AutoScaleManager.edit')
    def test_autoscale_edit_userfile(self, manager):
        # On windows, python cannot edit a NamedTemporaryFile.
        if (sys.platform.startswith("win")):
            self.skipTest("Test doesn't work in Windows")
        group = fixtures.SoftLayer_Scale_Group.getObject
        template = {
            'virtualGuestMemberTemplate': group['virtualGuestMemberTemplate']
        }
        template['virtualGuestMemberTemplate']['userData'] = [{'value': ''}]

        with tempfile.NamedTemporaryFile() as userfile:
            result = self.run_command(['autoscale', 'edit', '12345', '--userfile', userfile.name])
        self.assert_no_fail(result)
        manager.assert_called_with('12345', template)

    @mock.patch('SoftLayer.CLI.formatting.confirm')
    def test_autoscale_create(self, confirm_mock):
        confirm_mock.return_value = True
        result = self.run_command(['autoscale', 'create',
                                   '--name=test',
                                   '--cooldown=3600',
                                   '--min=1',
                                   '--max=3',
                                   '-o=CENTOS_7_64',
                                   '--datacenter=ams01',
                                   '--termination-policy=2',
                                   '-H=testvs',
                                   '-D=test.com',
                                   '--cpu=2',
                                   '--memory=1024',
                                   '--policy-relative=absolute',
                                   '--policy-amount=3',
                                   '--regional=102',
                                   '--disk=25'])
        self.assert_no_fail(result)
        self.assertEqual(result.exit_code, 0)

    def test_autoscale_delete(self):
        result = self.run_command(['autoscale', 'delete', '12345'])
        self.assert_no_fail(result)
