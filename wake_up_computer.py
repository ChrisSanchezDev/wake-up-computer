import asyncio
import os
import subprocess
from dotenv import load_dotenv
from logger import logger, console_logger
from wakeonlan import send_magic_packet

logger.info('-----STARTING SCRIPT: wake_up_computer.py-----')

load_dotenv()

IP_TYPE = os.getenv('IP_TYPE', 'local')
logger.debug(f'Environment loaded. IP_TYPE={IP_TYPE}')
if IP_TYPE == 'local':
    AVAILABLE_COMPUTERS = {
        'MSI': {'mac': os.getenv('MSI_MAC'), 'ip': os.getenv('MSI_LOCAL_IP')},
        'PI': {'mac': os.getenv('PI_MAC'), 'ip': os.getenv('PI_LOCAL_IP')},
        'TANK': {'mac': os.getenv('TANK_MAC'), 'ip': os.getenv('TANK_LOCAL_IP')},
        'TP': {'mac': os.getenv('TP_MAC'), 'ip': os.getenv('TP_LOCAL_IP')}
    }
elif IP_TYPE == 'tailscale':
    AVAILABLE_COMPUTERS = {
        'MSI': {'mac': os.getenv('MSI_MAC'), 'ip': os.getenv('MSI_TS_IP')},
        'PI': {'mac': os.getenv('PI_MAC'), 'ip': os.getenv('PI_TS_IP')},
        'TANK': {'mac': os.getenv('TANK_MAC'), 'ip': os.getenv('TANK_TS_IP')},
        'TP': {'mac': os.getenv('TP_MAC'), 'ip': os.getenv('TP_TS_IP')}
    }

def wake_device(computer: str):
    logger.info(f'Attempting to wake device {computer}...')
    
    computer = computer.upper()
    target = AVAILABLE_COMPUTERS.get(computer)
    
    if not target:
        logger.error(f'Error: The computer {computer} does not exist in the available computer dictionary.')
        return False
    elif not target['mac']:
        logger.error(f'Error: Could not collect MAC address from {computer}.')
        return False # Unsuccessful magic packet
    
    logger.debug(f'Resolved {computer} to MAC address: {target['mac']}')
    
    logger.info(f'Sending Magic Packet to {computer}...')
    send_magic_packet(target['mac'])
    return True

def check_status(computer: str):
    logger.info(f'Attempting to check device {computer}...')
    
    computer = computer.upper()
    target= AVAILABLE_COMPUTERS.get(computer)
    
    if not target:
        logger.error(f'Error: The computer {computer} does not exist in the available computer dictionary.')
        return False
    elif not target['ip']:
        logger.error(f'Error: Could not collect IP address from {computer}.')
        return False
    
    logger.debug(f'Resolved {computer} to IP address: {target['ip']}')
    
    param = '-n' if os.name == 'nt' else '-c' # 'nt' = Windows, 'posix' = Linux/macOS
    response = subprocess.call(
        ['ping', param, '1', '-W', '1', target['ip']],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if response >= 1:
        logger.info(f'Unfavorable response code from {computer}')
        logger.debug(f'Raw ping response code: {response}')
        logger.info(f'{computer} is still Offline, or there is a Ping error.')
    elif response == 0:
        logger.info(f'{computer} is Online!')
    
    return response == 0
    
async def wake_and_check(computer:str):
    console_logger.info(f'Attempting to wake and check {computer}...')
    target = AVAILABLE_COMPUTERS.get(computer)

    if not target:
        console_logger.error(f'Error: The computer {computer} does not exist in the available computer dictionary.')
        return
    elif not target['mac']:
        console_logger.error(f'Error: Could not collect MAC address from {computer}.')
        return
    
    console_logger.info(f'Sending Magic Packet to {computer}...')
    send_magic_packet(target['mac'])

    console_logger.info(f'Now waiting 45s to check for proper boot from {computer}...')

    # Check before timer so that we aren't wasting time
    if not target:
        console_logger.error(f'Error: The computer {computer} does not exist in the available computer dictionary.')
        return
    elif not target['ip']:
        console_logger.error(f'Error: Could not collect IP address from {computer}.')
        return
    
    await asyncio.sleep(45)
    console_logger.info(f'Attempting to ping {computer}...')
    
    param = '-n' if os.name == 'nt' else '-c' 
    response = subprocess.call(
        # ping: system command being called
        # param: count flag (-n, number of echo requests. -c, count of echo requests)
        # 1: Value for count flag
        # -W: Timeout flag
        # 1: Value for timeout flag (in seconds)
        # target['ip']: Destination IP address
        ['ping', param, '1', '-W', '1', target['ip']],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if response >= 1:
        # 1: Packet loss / request timed out
        # 2: Unknown host / network unreachable
        # 68: linux specific, host unreachable
        console_logger.info(f'Unfavorable response from {computer}')
        console_logger.debug(f'Raw ping response code: {response}')
        console_logger.info(f'{computer} is still Offline, or there is a Ping error.')
    elif response == 0:
        console_logger.info(f'{computer} is Online!')
    
    return

async def main(user_input:str):
    user_input = user_input.upper()
    commands = user_input.split(' ')

    tasks = []

    for computer in commands:
        if computer in AVAILABLE_COMPUTERS:
            tasks.append(wake_and_check(computer))

    if not tasks:
        console_logger.info('No valid computers found.')
        return
    
    await asyncio.gather(*tasks) # * Unpacks the task list into its parts (like MSI, PI, TANK)

if __name__ == '__main__':
    user_input = input('Input the computer(s) you want to wake up (MSI PI TANK TP):')
    asyncio.run(main(user_input))

#/home/chrissanchezdev/scripts/wake-up-computer/venv/bin/python3.13 wake_up_computer.py