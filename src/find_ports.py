import serial.tools.list_ports


def is_exoskeleton_conected():
    # if
    return "com3"


def find_com_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]  # Extract only COM port names


if __name__ == "__main__":
    ports = find_com_ports()
    if ports:
        print("Connected COM Ports:", ports)
    else:
        print("No COM ports detected.")
