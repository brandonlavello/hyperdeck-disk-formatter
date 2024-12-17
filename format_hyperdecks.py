import telnetlib
import time
import re
import sys
import threading

#Constants:
MAX_RETRIES = 3

def establish_connection(ip_address, port=9993):
    try:
        # Connect to the HyperDeck
        tn = telnetlib.Telnet(ip_address, port, timeout=5)

        # Receive and process the response
        response = tn.read_until(b'\n\r').decode('utf-8')

        return tn

    except (ConnectionRefusedError, ConnectionError, TimeoutError, OSError) as e:
        print(f"Error connecting to HyperDeck: {e}")
        return None
    
def get_slot_count(tn):
    try:
        # Send the command
        tn.write(b'device info\n')

        # Receive and process the response
        response = tn.read_until(b'\n\r').decode('utf-8')

        # Extract the slot count from the response
        slot_count = None
        lines = response.strip().split('\n')
        for line in lines:
            if line.startswith('slot count:'):
                slot_count = int(line.split(': ')[1])
                break

        if slot_count is not None:
            # print(f"Slot count: {slot_count}")
            return slot_count
        else:
            print("Slot count not found in device info response.")

    except (ConnectionRefusedError, ConnectionError) as e:
        print(f"Error receiving device info: {e}")


def get_slot_data(tn,slot_count):
    responses = []
    for i in range(slot_count):
        try:
            # Send the command
            tn.write(b'slot info: slot id: ' + str(i+1).encode() + b'\n')

            # Receive and process the response
            response = tn.read_until(b'\n\r').decode('utf-8')

            # print(f"Response from HyperDeck: {response.strip()}")
            # print("\n\n")
            response = response.strip()  # You can return the response for further processing if needed
            responses.append(response)
            # return response

        except (ConnectionRefusedError, ConnectionError) as e:
            print(f"Error receiving slot data: {e}")
            return None
    return responses


def filter_slot_data(tn, slot_count, slot_data):
    try:
        disks = []

        for i in range(slot_count):
            slot_info = slot_data[i]
            if slot_info is not None:
                if 'status: empty' not in slot_info:
                    
                    disks.append(slot_info)
            else:
                print("Failed to retrieve slot information.")

    except Exception as e:
        print(f"An error occurred: {e}")

    return disks

def format_all_slots(tn,disks,ip_address):
    # Define a regular expression pattern to match the slot ID
    pattern = r'slot id: (\d+)'
    format_command = b'format: prepare: HFS+\n'
    format_disks = []

    for i in range(len(disks)):
        # Use re.search to find the first occurrence of the pattern in the input string
        match = re.search(pattern, disks[i])

        # Check if a match was found
        if match:
            # Extract the slot ID from the matched group
            slot_id = match.group(1)
            # print(f"Slot ID: {slot_id}")
            format_disks.append(slot_id)
        else:
            print("Slot ID not found in the input string.")
    
    for i in range(len(format_disks)):
        # print('slot select: slot id: ' + str(format_disks[i]) + '\n')
        tn.write(b'slot select: slot id: ' + str(format_disks[i]).encode() + b'\n')
        
        # Receive and process the response
        response = tn.read_until(b'ok').decode('utf-8')
        response = response.strip()  # You can return the response for further processing if needed
        # print("Select response: " + response)

        tn.write(format_command)
        
        # Receive and process the response
        response = tn.read_until(b'\n\r').decode('utf-8')
        response = response.replace("216 format ready:", "").strip()
        # print("code: " + response)

        tn.write(b'format: confirm: ' + response.encode() + b'\n')

        # Receive and process the response
        response = tn.read_until(b'ok').decode('utf-8')
        response = response.strip()  # You can return the response for further processing if needed
        if response == "200 ok":
            print("HyperDeck{} :  - Format Successful on slot {}".format(ip_address,format_disks[i]))
        else:
            print("Error: HyperDeck{} :Format Unsuccessful on slot: {}".format(ip_address,format_disks[i]))

def connect_and_format(ip_address):
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Attempt {attempt} to connect...")
        tn = establish_connection(ip_address)

        if tn is not None:
            print("Connection to: {} successful!".format(ip_address) )
            break
        else:
            print("Retrying in 3 seconds...")
            time.sleep(3)
        if attempt == 3:
            print("Error Establishing Connection.  Check Network Status.")
            sys.exit()

    slot_count = get_slot_count(tn)
    slot_data = get_slot_data(tn, slot_count)
    filtered_slot_data = filter_slot_data(tn,slot_count,slot_data)


    format_all_slots(tn,filtered_slot_data,ip_address)

    # Close the Telnet connection when done
    tn.close()

if __name__ =="__main__":

    # Example usage:
    ip_address1 = '10.10.10.31'  # Replace with your HyperDeck's IP address
    ip_address2 = '10.10.10.32'
    ip_address3 = '10.10.10.33'
    ip_address4 = '10.10.10.34'

    # creating thread
    t1 = threading.Thread(target=connect_and_format, args=(ip_address1,))
    t2 = threading.Thread(target=connect_and_format, args=(ip_address2,))
    t3 = threading.Thread(target=connect_and_format, args=(ip_address3,))
    t4 = threading.Thread(target=connect_and_format, args=(ip_address4,))

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
    # starting thread 3
    t3.start()
    # starting thread 4
    t4.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
    # wait until thread 1 is completely executed
    t3.join()
    # wait until thread 2 is completely executed
    t4.join()


    # both threads completely executed
    print("Done!")

    exit()