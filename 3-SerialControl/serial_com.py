#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial

port = "/dev/ttyACM0"
broadcast_id = 0xFE
present_position_addr = 0x24
led_addr = 0x19
def open_serial(port, baud, timeout):
    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
    if ser.isOpen():
        return ser
    else:
        ser.open()
        if not ser.isOpen():
            print("SERIAL ERROR")


def close(ser):
    ser.close()

def open(ser):
    ser.open()


def write_data(ser, data):
    ser.write(data)


def read_data(ser, size=1):
    return ser.read(size)


def to_hex(val):
    return chr(val)


def decode_data(data):
    res = ""
    for d in data:
        res += hex(d) + " "

    return res


def checksum(data):
    return (~data) & 0xff

def read_present_position(ser, motor_id):
    # motor_id = id of the motor
    # lenght = lenght of the packet
    # instruction read = 0x02
    # param1 = addr to read
    # param2 = lenght of data read
    data = serial_data(motor_id, 0x04, 0x02, present_position_addr, 0x02)
    print(decode_data(data))
    write_data(serial_port, data)
    return read_data(ser, 2)

def serial_data(motor_id=0xFE, lenght=0x04, instruction=0x03, param1=0x19, param2=0x01): # without parameters : LED on 

    # we create the packet for a LED ON command
    # two start bytes
    data_start = 0xff

    # id of the motor 
    data_id = motor_id

    # lenght of the packet
    data_lenght = lenght

    # instruction write= 0x03
    data_instruction = instruction

    # instruction parameters
    data_param1 = param1 # LED address=0x19
    data_param2 = param2  # write 0x01

    # checksum (read the doc)
    data_checksum = checksum(
        data_id
        + data_lenght
        + data_instruction
        + data_param1
        + data_param2
    )

    print("checksum = {}".format(data_checksum))

    # we concatenate everything
    data = bytes([
        data_start,
        data_start,
        data_id,
        data_lenght,
        data_instruction,
        data_param1,
        data_param2,
        data_checksum
    ])
    return data


if __name__ == "__main__":

    # we open the port
    serial_port = open_serial(port, 1000000, timeout=0.1)

    # we create the packet for a LED ON command
    # two start bytes
    data_start = 0xff

    # id of the motor 
    data_id = 0xFE

    # lenght of the packet
    data_lenght = 0x04

    # instruction write= 0x03
    data_instruction = 0x03

    # instruction parameters
    data_param1 = 0x19 # LED address=0x19
    data_param2 = 0x01  # write 0x01

    # checksum (read the doc)
    data_checksum = checksum(
        data_id
        + data_lenght
        + data_instruction
        + data_param1
        + data_param2
    )

    print("checksum = {}".format(data_checksum))

    # we concatenate everything
    data = bytes([
        data_start,
        data_start,
        data_id,
        data_lenght,
        data_instruction,
        data_param1,
        data_param2,
        data_checksum
    ])

    print(decode_data(data))
    write_data(serial_port, data)

    # read the status packet (size 6)
    d = read_data(serial_port, 6)
    print(decode_data(d))
    read_present_position(serial_port, data_id)