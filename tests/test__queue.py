#!/usr/bin/env python3
#-*- coding: UTF-8 -*-


"""
Queue test cases
"""

from lib.queue import VlanQueue
import unittest

VLANS =    [(0, 1, 2), (0, 1, 5), (0, 1, 8), (0, 0, 2), (0, 0, 3), (0, 0, 4),
            (0, 0, 6), (0, 0, 7), (0, 0, 8), (0, 0, 10), (1, 1, 1), (1, 1, 5),
            (1, 1, 6), (1, 1, 9), (1, 0, 1), (1, 0, 4), (1, 0, 5), (1, 0, 7),
            (2, 1, 1), (2, 1, 4), (2, 1, 10)]

REQUESTS = [(0, 1), (1, 0), (2, 1), (3, 0), (4, 1)]

OUTPUT   = [(0, 1, 0, 1), (0, 1, 1, 1), (1, 2, 1, 1), (2, 0, 0, 2),
            (2, 0, 1, 2), (3, 2, 1, 4), (4, 1, 0, 5), (4, 1, 1, 5)]


class TestQueue(unittest.TestCase):
    """
    Tests the given example
    """

    def setUp(self):
        self.queue = VlanQueue()
        queue = self.queue
        for vlan in VLANS:
            queue.push_vlan(*vlan)

    def test__queue__first_item_is_smallest(self):
        queue = self.queue
        self.assertEqual(queue.primary_heap[0], (1, 1))

    def test__queue__all_primaries_are_added(self):
        queue = self.queue
        primaries = sum(1  for _,primary,_ in VLANS  if primary)
        self.assertEqual(len(queue.primary_heap), primaries)

    def test__queue__all_secondaries_are_added(self):
        queue = self.queue
        secondaries = sum(1  for _,primary,_ in VLANS  if not primary)
        self.assertEqual(len(queue.secondary), secondaries)

    def test__queue__smallest_is_poped(self):
        queue = self.queue
        first_vlan = queue.get_vlans()[0]
        second_vlan = queue.get_vlans()[0]
        self.assertNotEqual(first_vlan, second_vlan)

    def test__queue__smallest_is_restored(self):
        queue = self.queue
        first_vlan = queue.get_vlans()[0]
        second_vlan = queue.get_vlans()[0]
        queue.push_vlan(*first_vlan)
        third_vlan = queue.get_vlans()[0]
        self.assertEqual(first_vlan, third_vlan)

    def test__queue__raises_valueerror_when_emptied(self):
        queue = self.queue
        primaries = sum(1  for _,primary,_ in VLANS  if primary)
        with self.assertRaises(ValueError):
            for attempt in range(primaries + 1):
                vlan = queue.get_vlans()

    def test__queue__consistent_with_sample_output(self):
        queue = self.queue
        expected_sequence = []
        for request, device, primary, vlan in OUTPUT:
            expected_sequence.append((device, primary, vlan))

        output_sequence = []
        for request, primary in REQUESTS:
            for vlan_uid in queue.get_vlans(primary):
                device, vlan, primary = vlan_uid
                output_sequence.append((device, primary, vlan))

        self.assertEqual(output_sequence, expected_sequence)

