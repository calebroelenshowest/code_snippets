import pyModbusTCP
import struct
from pyModbusTCP.client import ModbusClient


class ModbusClientWrapper(ModbusClient):
    """Wrapper for ModbusClient to make project easier.\n
        Constructor

        Modbus server params (host, port) can be set here or with host(), port()
        functions. Same for debug option.

        :param host: hostname or IPv4/IPv6 address server address (optional)
        :type host: str
        :param port: TCP port number (optional)
        :type port: int
        :param unit_id: unit ID (optional)
        :type unit_id: int
        :param timeout: socket timeout in seconds (optional)
        :type timeout: float
        :param debug: debug state (optional)
        :type debug: bool
        :return: Object ModbusClient
        :rtype: ModbusClient
        :raises ValueError: if a set parameter value is incorrect
    """

    def __init__(self, host: str, unit_id: int, port: int, debugging: bool = False, timeout: float = 10,
                 logging_prefix: str = "ModbusClient:"):
        super().__init__(host=host, unit_id=unit_id, port=port, auto_open=False, timeout=timeout, debug=debugging)

        self.__logging_prefix = logging_prefix + " " * (len(logging_prefix) > 0)
        self.connection_status = self.open()
        if not self.connection_status:
            print(f"{self.__logging_prefix}Failed to connect to Modbus!")
            print(f"{self.last_error()}")

    def reconnect(self) -> bool:
        """
        Try to connect again.
        :return: Reconnect status
        """
        self.connection_status = self.open()
        return self.connection_status

    def printl(self, message: str):
        """
        Alternative print statement that adds prefix. \n
        :param message:
        :return:
        """
        print(f"{self.__logging_prefix}{message}")

    def read_value_raw(self, register_index: int, register_count: int):
        data = self.read_holding_registers(register_index, register_count)
        if data is None:
            self.printl("Register does not exist.")
            return None
        return data

    @staticmethod
    def convert_to_int_2word(data):
        value = data[0] << 16 | data[1]
        if value & 0x80000000:
            value -= 2 ** 32
        return value/32786

    @staticmethod
    def convert_to_int_1word(data):
        value = data[0]
        if value & 0x80:
            value -= 2 ** 16
        return value/4096


c = ModbusClientWrapper(host='', unit_id=255, port=502, debugging=False, timeout=5)

for x in range(0, 30, 2):
    new_data = c.read_value_raw(0, 8)
    # print(new_data)
    # v = c.convert_to_int_2word(new_data)

