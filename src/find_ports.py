import serial.tools.list_ports


def describe_com_port(target_port):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.device == target_port:
            print(f"Port:        {port.device}")
            print(f"Description: {port.description}")
            print(f"HWID:        {port.hwid}")
            print(f"Manufacturer:{port.manufacturer}")
            print(f"Serial No:   {port.serial_number}")
            return port
    print(f"{target_port} not found.")


def is_exoskeleton_connected(simulate_pass=False, simulate_fail=False):
    if simulate_pass:
        return "COM3"
    elif simulate_fail:
        return None

    ports = serial.tools.list_ports.comports()

    matching_ports = [
        port.device
        for port in ports
        if (
            "0403:6001" in port.hwid
            or "FTDI" in (port.manufacturer or "")
            or "USB Serial Port" in port.description
        )
    ]

    if len(matching_ports) == 1:
        return matching_ports[0]
    elif len(matching_ports) > 1:
        raise Exception(
            "Multiple devices matching exoskeleton signature detected. Please disconnect all other devices and try again."
        )
    else:
        return None


def find_com_ports():
    ports = serial.tools.list_ports.comports()
    # print("HERE:) ")
    print(port.description for port in ports)
    return [port.device for port in ports]  # Extract only COM port names


if __name__ == "__main__":
    ports = find_com_ports()
    describe_com_port("COM3")
    if ports:
        print("Connected COM Ports:", ports)
    else:
        print("No COM ports detected.")
    print(f"Where is the Exoskeleton Connected?  {is_exoskeleton_connected()}")
