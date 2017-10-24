import os
import unittest
import yaml
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.test import TestCase
from lxml import etree
from pyvcloud.vcd.client import TaskStatus

class TestDiskSetup(TestCase):


    def test_012_add_disk(self):

        logged_in_org = self.client.get_org()
       
        org = Org(self.client, resource=logged_in_org)
        v = org.get_vdc(self.config['vcd']['vdc'])
        vdc = VDC(self.client, href=v.get('href'))
        
        #taskObj = vdc.add_disk(self.config['vcd']['disk'], "10", None, None, '10 MB Disk', self.config['vcd']['storage_profile'])
        taskObj = vdc.add_disk(self.config['vcd']['disk'], "10", None, None, '10 MB Disk')
        task = self.client.get_task_monitor().wait_for_status(
                                task=taskObj,
                                timeout=30,
                                poll_frequency=2,
                                fail_on_status=None,
                                expected_target_statuses=[
                                    TaskStatus.SUCCESS,
                                    TaskStatus.ABORTED,
                                    TaskStatus.ERROR,
                                    TaskStatus.CANCELED],
                                callback=None)
        assert task.get('status') == TaskStatus.SUCCESS.value


if __name__ == '__main__':
    unittest.main()