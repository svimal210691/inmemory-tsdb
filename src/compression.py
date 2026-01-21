import base64
import sys
import zlib
from typing import List
from datetime import datetime


class CompressionUtil:

    def __init__(self):
        pass

    @staticmethod
    def compress_list_simple(data:List[int]) -> str:
        data_str = ",".join([str(i) for i in data])
        bytes_data = data_str.encode('utf-8')

        # Get original size
        original_size = sys.getsizeof(bytes_data)
        print(f"Original size: {original_size} bytes")

        # Compress the data
        compressed_data = zlib.compress(bytes_data)

        # Get compressed size
        compressed_size = sys.getsizeof(compressed_data)
        print(f"Compressed size: {compressed_size} bytes")
        print(f"Percent compression: {((original_size - compressed_size) * 100)/ original_size}")

        encoded_string = base64.b64encode(compressed_data).decode('utf-8')
        return encoded_string

    @staticmethod
    def compress_list_after_xor(data:List[int]) -> str:
        for i in range(1, len(data)):
            data[i] = data[i] ^ data[0]
        return CompressionUtil.compress_list_simple(data)


    @staticmethod
    def compress_timestamps(data:List[datetime]) -> str:
        data_str = ",".join([str(i) for i in data])
        bytes_data = data_str.encode('utf-8')

        # Get original size
        original_size = sys.getsizeof(bytes_data)
        print(f"Original size: {original_size} bytes")

        # Compress the data
        compressed_data = zlib.compress(bytes_data)

        # Get compressed size
        compressed_size = sys.getsizeof(compressed_data)
        print(f"Compressed size: {compressed_size} bytes\n")
        print(f"Percent compression: {((original_size - compressed_size) * 100) / original_size}")

        encoded_string = base64.b64encode(compressed_data).decode('utf-8')
        return encoded_string

    @staticmethod
    def compress_timestamps_delta(data:List[datetime]) -> str:
        delta_list = [data[i].minute - data[i - 1].minute for i in range(1, len(data))]
        delta_of_delta_list = ",".join([str(delta_list[i] - delta_list[i - 1]) for i in range(1, len(delta_list))])
        bytes_data = delta_of_delta_list.encode('utf-8')

        # Get original size
        original_size = sys.getsizeof(bytes_data)
        print(f"Original size: {original_size} bytes")

        # Compress the data
        compressed_data = zlib.compress(bytes_data)

        # Get compressed size
        compressed_size = sys.getsizeof(compressed_data)
        print(f"Compressed size: {compressed_size} bytes")
        print(f"Percent compression: {((original_size - compressed_size) * 100) / original_size}")

        encoded_string = base64.b64encode(compressed_data).decode('utf-8')
        return encoded_string
