# 复杂数据类型

from collections import OrderedDict
import logging

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder



ORDER_DICT = {"<": "LITTLE", ">": "BIG"}


def run_binary_payload_client(host:str,port:int):
    client = ModbusClient(host,port)
  
    for word_endian, byte_endian in (
        (Endian.Big, Endian.Big),
        (Endian.Big, Endian.Little),
        (Endian.Little, Endian.Big),
        (Endian.Little, Endian.Little),
    ):
        print("-" * 60)
        print(f"Word Order: {ORDER_DICT[word_endian]}")
        print(f"Byte Order: {ORDER_DICT[byte_endian]}")
        print()
    
        builder = BinaryPayloadBuilder(
            wordorder=word_endian,
            byteorder=byte_endian,
        )
		
		# 写入的变量
        my_string = "abcd-efgh123345765432"
        builder.add_string(my_string)
        builder.add_bits([0, 1, 0, 1, 1, 0, 1, 0])
        builder.add_8bit_int(-0x12)
        builder.add_8bit_uint(0x12)
        builder.add_16bit_int(-0x5678)
        builder.add_16bit_uint(0x1234)
        builder.add_32bit_int(-0x1234)
        builder.add_32bit_uint(0x12345678)
        builder.add_16bit_float(12.34)
        builder.add_16bit_float(-12.34)
        builder.add_32bit_float(22.34)
        builder.add_32bit_float(-22.34)
        builder.add_64bit_int(-0xDEADBEEF)
        builder.add_64bit_uint(0x12345678DEADBEEF)
        builder.add_64bit_uint(0x12345678DEADBEEF)
        builder.add_64bit_float(123.45)
        builder.add_64bit_float(-123.45)
        registers = builder.to_registers()
        print("Writing Registers:")
        print(registers)
        print("\n")
        payload = builder.build()
        address = 40001          # 从40001开始写入
        # We can write registers
        client.write_registers(address, registers, unit=1)    # 写入
     	
     	# 读取复杂变量
        print("Reading Registers:")
        address = 40001

        count = len(payload)
        print(f"payload_len {count}")
        result = client.read_holding_registers(address, count, slave=1)
        print(result.registers)
        print("\n")
        decoder = BinaryPayloadDecoder.fromRegisters(
            result.registers, byteorder=byte_endian, wordorder=word_endian
        )
        # Make sure word/byte order is consistent between BinaryPayloadBuilder and BinaryPayloadDecoder
        assert (
            decoder._byteorder == builder._byteorder  # pylint: disable=protected-access
        )  # nosec
        assert (
            decoder._wordorder == builder._wordorder  # pylint: disable=protected-access
        )  # nosec

        decoded = OrderedDict(
            [
                ("string", decoder.decode_string(len(my_string))),
                ("bits", decoder.decode_bits()),
                ("8int", decoder.decode_8bit_int()),
                ("8uint", decoder.decode_8bit_uint()),
                ("16int", decoder.decode_16bit_int()),
                ("16uint", decoder.decode_16bit_uint()),
                ("32int", decoder.decode_32bit_int()),
                ("32uint", decoder.decode_32bit_uint()),
                ("16float", decoder.decode_16bit_float()),
                ("16float2", decoder.decode_16bit_float()),
                ("32float", decoder.decode_32bit_float()),
                ("32float2", decoder.decode_32bit_float()),
                ("64int", decoder.decode_64bit_int()),
                ("64uint", decoder.decode_64bit_uint()),
                ("ignore", decoder.skip_bytes(8)),
                ("64float", decoder.decode_64bit_float()),
                ("64float2", decoder.decode_64bit_float()),
            ]
        )
        print("Decoded Data")
        for name, value in iter(decoded.items()):
            print(
                "%s\t" % name,  # pylint: disable=consider-using-f-string
                hex(value) if isinstance(value, int) else value,
            )
        print("\n")

	# 关闭连接
    client.close()


if __name__ == "__main__":
    run_binary_payload_client("127.0.0.1", 503)    
