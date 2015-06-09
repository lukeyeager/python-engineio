import unittest

import six

from engineio import packet


class TestPacket(unittest.TestCase):
    def test_encode_default_packet(self):
        pkt = packet.Packet()
        self.assertEqual(pkt.packet_type, packet.NOOP)
        self.assertIsNone(pkt.data)
        self.assertFalse(pkt.binary)
        self.assertEqual(pkt.encode(), b'6')

    def test_decode_default_packet(self):
        pkt = packet.Packet(encoded_packet=b'6')
        self.assertTrue(pkt.encode(), b'6')

    def test_encode_text_packet(self):
        pkt = packet.Packet(packet.MESSAGE, data='text')
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, 'text')
        self.assertFalse(pkt.binary)
        self.assertEqual(pkt.encode(), b'4text')

    def test_decode_text_packet(self):
        pkt = packet.Packet(encoded_packet=b'4text')
        self.assertTrue(pkt.encode(), b'text')

    def test_encode_binary_packet(self):
        pkt = packet.Packet(packet.MESSAGE, data=b'\x01\x02\x03',
                            binary=True)
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, b'\x01\x02\x03')
        self.assertTrue(pkt.binary)
        self.assertEqual(pkt.encode(), b'\x04\x01\x02\x03')

    def test_encode_binary_b64_packet(self):
        pkt = packet.Packet(packet.MESSAGE, data=b'\x01\x02\x03\x04',
                            binary=True)
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, b'\x01\x02\x03\x04')
        self.assertTrue(pkt.binary)
        self.assertEqual(pkt.encode(b64=True), b'b4AQIDBA==')

    @unittest.skipIf(six.PY2,
                     'automatic binary detection not support in Python 2')
    def test_encode_binary_packet_py3(self):
        pkt = packet.Packet(packet.MESSAGE, data=b'\x01\x02\x03')
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, b'\x01\x02\x03')
        self.assertTrue(pkt.binary)
        self.assertEqual(pkt.encode(), b'\x04\x01\x02\x03')

    def test_decode_binary_packet(self):
        pkt = packet.Packet(encoded_packet=b'\x04\x01\x02\x03')
        self.assertTrue(pkt.encode(), b'\x04\x01\x02\x03')

    def test_decode_binary_b64_packet(self):
        pkt = packet.Packet(encoded_packet=b'b4AAEC')
        self.assertTrue(pkt.encode(), b'\x04\x01\x02\x03')

    def test_encode_json_packet(self):
        pkt = packet.Packet(packet.MESSAGE, data={'a': 123, 'b': '456'})
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, {'a': 123, 'b': '456'})
        self.assertFalse(pkt.binary)
        self.assertIn(pkt.encode(), [b'4{"a":123,"b":"456"}',
                                     b'4{"b":"456","a":123}'])

    def test_decode_json_packet(self):
        pkt = packet.Packet(encoded_packet=b'4{"a":123,"b":"456"}')
        self.assertIn(pkt.encode(), [b'4{"a":123,"b":"456"}',
                                     b'4{"b":"456","a":123}'])

    def test_encode_number_packet(self):
        pkt = packet.Packet(packet.MESSAGE, data=123)
        self.assertEqual(pkt.packet_type, packet.MESSAGE)
        self.assertEqual(pkt.data, 123)
        self.assertFalse(pkt.binary)
        self.assertEqual(pkt.encode(), b'4123')
