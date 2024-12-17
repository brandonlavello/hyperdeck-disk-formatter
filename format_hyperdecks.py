import socket
import time
import re
import sys
import threading

# Constants:
MAX_RETRIES = 3

def establish_connection(ip_address, port=9993):
    try:
        # Create a socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ip_address, port))

        # Receive and process the response
        response = s.recv(1024).decode('utf-8').strip()
        return s

    except (socket.error, socket.timeout) as e:
        print(f"Error connecting to HyperDeck: {e}")
        return None

def send_command(s, command):
    try:
        s.sendall(command.encode() + b'\n')
        response = s.recv(1024).decode('utf-8').strip()
        return response
    except (socket.error, socket.timeout) as e:
        print(f"Error sending command '{command}': {e}")
        return None

def get_slot_count(s):
    response = send_command(s, 'device info')
    if response:
        # Extract the slot count from the response
        lines = response.split('\n')
        for line in lines:
            if line.startswith('slot count:'):
                return int(line.split(': ')[1])
    print("Slot count not found in device info response.")
    return 0

def get_slot_data(s, slot_count):
    responses = []
    for i in range(slot_count):
        response = send_command(s, f'slot info: slot id: {i + 1}')
        if response:
            responses.append(response.strip())
    return responses

def filter_slot_data(slot_count, slot_data):
    disks = []
    for i in range(slot_count):
        slot_info = slot_data[i]
        if 'status: empty' not in slot_info:
            disks.append(slot_info)
    return disks

def format_all_slots(s, disks, ip_address):
    pattern = r'slot id: (\d+)'
    format_command = 'format: prepare: HFS+'

    format_disks = [
        match.group(1)
        for disk in disks
        if (match := re.search(pattern, disk))
    ]

    for slot_id in format_disks:
        send_command(s, f'slot select: slot id: {slot_id}')
        response = send_command(s, format_command).replace("216 format ready:", "").strip()
        final_response = send_command(s, f'format: confirm: {response}')

        if final_response == "200 ok":
            print(f"HyperDeck {ip_address}: - Format Successful on slot {slot_id}")
        else:
            print(f"Error: HyperDeck {ip_address}: Format Unsuccessful on slot {slot_id}")

def connect_and_format(ip_address):
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Attempt {attempt} to connect...")
        s = establish_connection(ip_address)

        if s:
            print(f"Connection to: {ip_address} successful!")
            break
        else:
            print("Retrying in 3 seconds...")
            time.sleep(3)
        if attempt == MAX_RETRIES:
            print("Error Establishing Connection. Check Network Status.")
            sys.exit()

    slot_count = get_slot_count(s)
    slot_data = get_slot_data(s, slot_count)
    filtered_slot_data = filter_slot_data(slot_count, slot_data)

    format_all_slots(s, filtered_slot_data, ip_address)

    # Close the socket connection when done
    s.close()

if __name__ == "__main__":
    # Example usage:
    ip_address1 = '10.10.10.31'
    ip_address2 = '10.10.10.32'
    ip_address3 = '10.10.10.33'
    ip_address4 = '10.10.10.34'

    # Creating threads
    t1 = threading.Thread(target=connect_and_format, args=(ip_address1,))
    t2 = threading.Thread(target=connect_and_format, args=(ip_address2,))
    t3 = threading.Thread(target=connect_and_format, args=(ip_address3,))
    t4 = threading.Thread(target=connect_and_format, args=(ip_address4,))

    # Starting threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    # Wait until threads are completely executed
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    print("Done!")
    exit()
