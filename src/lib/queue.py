#!/usr/bin/env python3
#-*- coding: UTF-8 -*-


"""
Queue Data structures that adds Vlan allocation logic
"""

from heapq import heappop, heappush


class VlanQueue:

    def __init__(self):
        """
        It uses heap queues to keep the order of assignation in references
        lists. This allows fast creation/access. The duplicates in diferent
        references lists are not expensive since they only keep the reference
        to an already existing vlan object.
        """
        self.primary_heap = []
        self.redundant_heap = []
        self.secondary = []
        self.available = set()

    def push_vlan(self, device_id, is_primary, vlan_id):
        """
        Registers a avaliable device's vlan id.
        It creates a vlan object which is shared in the diferents queues taking
        advantage of mutables and reference asignation behaviour in python.
        """

        vlan_uid = (vlan_id, device_id)
        self.available.add(vlan_uid)

        if is_primary:
            heappush(self.primary_heap, vlan_uid)
            if vlan_uid in self.secondary:
                heappush(self.redundant_heap, vlan_uid)
        else:
            self.secondary.append(vlan_uid)
            if vlan_uid in self.primary_heap:
                heappush(self.redundant_heap, vlan_uid)


    def get_vlans(self, redundant=False):
        """
        Returns a list of port that'll fullfil the query.
        The list will have two ports if asked for a redundant allocation.
        """
        if redundant:
            heap = self.redundant_heap
        else:
            heap = self.primary_heap

        while heap:
            vlan = heappop(heap)
            if vlan in self.available:
                self.available.remove(vlan)
                vlan_id, device_id = vlan
                break
        else:
            raise ValueError("Queue was emptied")

        if redundant:
            types = (0, 1)
        else:
            types = (1,)

        return [[device_id, vlan_id, is_primary]  for is_primary in types]
