import asyncio
import os
import subprocess
from dotenv import load_dotenv
from wakeonlan import send_magic_packet

load_dotenv()

AVAILABLE_COMPUTERS = {
    'MSI': {'mac': os.getenv('MSI_MAC'), 'ip': os.getenv('MSI_IP')},
    'PI': {'mac': os.getenv('PI_MAC'), 'ip': os.getenv('PI_IP')},
    'TANK': {'mac': os.getenv('TANK_MAC'), 'ip': os.getenv('TANK_IP')},
    'TP': {'mac': os.getenv('TANK_MAC'), 'ip': os.getenv('TANK_IP')}
}

async def wake_and_check(computer:str):
    target = AVAILABLE_COMPUTERS.get(computer)

    if not target or not target['mac']:
        print(f'Error: Could not collect mac address from {computer}.')
        return
    print(f'Sending Magic Packet to {computer}...')
    send_magic_packet(target['mac'])

    print(f'Now waiting 45s to check for proper boot from {computer}...')
    await asyncio.sleep(45)

    print(f'Attempting to ping {computer}...')
    param = '-n' if os.name == 'nt' else '-c' # Windows machines are considered nt machines in the os.name (os from import os)
    if not target['ip']:
        print(f'Error: Could not collect ip address from {computer}.')
        return
    process = await asyncio.create_subprocess_exec(
        'ping', param, '1', target['ip'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return_code = await process.wait()

    if return_code == 0:
        print(f'{computer} is Online!')
    else:
        print(f'Error: {computer} is still Offline. Code: {return_code}')


async def main(user_input:str):
    user_input = user_input.upper()
    commands = user_input.split(' ')

    tasks = []

    for computer in commands:
        if computer in AVAILABLE_COMPUTERS:
            tasks.append(wake_and_check(computer))

    if not tasks:
        print('No valid computers found.')
        return
    
    await asyncio.gather(*tasks) # * Unpacks the task list into its parts (like MSI, PI, TANK)
    
if __name__ == '__main__':
    user_input = input('Input the computer(s) you want to wake up (MSI PI TANK TP):')
    asyncio.run(main(user_input))

#/home/chrissanchezdev/scripts/wake-up-computer/venv/bin/python3.13 wake_up_computer.py