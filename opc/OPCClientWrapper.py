import opcua
from opcua import Client as OPCClient
from opcua import ua
from opcua.common import ua_utils
from opcua.ua.uaerrors import BadTypeMismatch
import ping3


class OPCNode:
    """Node paths for the OPC application\n"""
    HEATING_SETPOINT = ""
    """Node for the activation point for the heating."""
    HEATING_TEMP_REACTOR = ""
    """Node for the current temperature of the reactor (room)."""
    DIGITAL_INPUT_0 = ""
    """Node for Switch 0 (Coil 0)"""
    DIGITAL_INPUT_1 = ""
    """Node for Switch 1 (Coil 1)"""
    DIGITAL_OUTPUT_0 = ""
    """Node for Digital Output 0 """
    DIGITAL_OUTPUT_1 = ""
    """Node for Digital Input 1"""
    RESET_OUTPUT_4 = ""
    """Node for Reset 4 (Coil 4)"""
    SET_OUTPUT_4 = ""
    """Node for Set 3 (Coil 4)"""
    SWITCH_OUTPUT_3 = ""
    """Node for Switch 4 (Coil 3)"""
    SWITCH_OUTPUT_5 = ""
    """Node for Switch 5 (Coil 5)"""
    

class OPCClientWrapper(OPCClient):
    """Wraps the OPCClient, adds more project specific functionality to the application.\n
    Doesn't use real logging, just print statements.\n"""

    def __init__(self, logging_prefix="", *args, **kwargs):
        """
        :param logging_prefix: Prefix for the logging, if empty -> Ignored
        :param args: Args, inherited
        :param kwargs: Kwargs, inherited
        """
        super().__init__(*args, **kwargs)
        # Add a space if logging_prefix exists
        self.__logging_prefix = logging_prefix + " " * (logging_prefix != "")
        print(f"{self.__logging_prefix}Connecting to {self.server_url.netloc} using protocol {self.server_url.scheme}")
        self.__connected = False
        try:
            self.connect()
            self.__connected = True
        except Exception as connect_error:
            print(f"{self.__logging_prefix}Failed to connect to server: {connect_error}")
            print(f"{self.__logging_prefix}Try again using _.reconnect()")
            self.__connected = False

    @property
    def is_connected(self):
        """Is the client connect? If not: self.reconnect()\n"""
        return self.__connected

    @property
    def is_reachable(self):
        """Is the given IP reachable? Doesn't check if there is a server!"""
        # Remove the port first
        no_port_ip = self.server_url.netloc[:str(self.server_url.netloc).index(":")]
        # Ping to this IP: Response in ms
        ping_response_time_ms = ping3.ping(no_port_ip)
        return ping_response_time_ms is not None

    def reconnect(self) -> bool:
        """
        Reconnect to the server
        :return: Success state
        """
        print(f"{self.__logging_prefix}Connecting to {self.server_url.netloc} using protocol {self.server_url.scheme}")
        try:
            self.connect()
            print(f"{self.__logging_prefix}Connection success")
            return True
        except Exception as connect_error:
            print(f"{self.__logging_prefix}Failed to connect to server: {connect_error}")
            print(f"{self.__logging_prefix}Try again using _.reconnect()")
            return False

    def get_node_datavalue(self, node: str):
        """
        Get data from a node.\n
        :param node: Node from OPCNode
        :return: Data node (type DataValue Node)
        """
        node = self.get_node(node)
        return node.get_data_value()

    def get_node_value(self, node: str):
        """
        Get data from node. \n
        :param node: Node from OPCNode
        :return: Data from the node itself (Python)
        """
        node = self.get_node(node)
        return node.get_value()

    def write_node_value(self, node_name: str, value):
        """
        Write a value to a node
        :param node_name: Node to write to
        :param value: Value to apply
        :return: Success status
        """
        # Steps:
        # Convert the data to a DataValue
        # Remove the TimeStamp
        # Apply
        varianttype = None
        node = self.get_node(node_name)
        dv = self.convert_to_datavalue(value)
        try:
            self.set_values([node], [dv])
        except BadTypeMismatch as btm:
            print(f"This node does not support the given type: {type(value).__name__}")
            print(f"Required type: {node.get_data_value().Value.VariantType}")

    @staticmethod
    def convert_to_datavalue(value) -> ua.DataValue:
        """
        Convert a python type to a datavalue\n
        :param value: The pythonic value
        :return: The ua.Datavalue object
        """
        if type(value) == float:
            return ua.DataValue(ua.Variant(value, ua.VariantType.Float), serverTimestamp=None, sourceTimestamp=None)
        if type(value) == int:
            return ua.DataValue(ua.Variant(value, ua.VariantType.UInt16), serverTimestamp=None, sourceTimestamp=None)
