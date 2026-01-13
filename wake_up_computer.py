import os
from wakeonlan import send_magic_packet
from dotenv import load_dotenv

load_dotenv()

MSI_MAC = os.getenv('MSI_MAC')
PI_MAC = os.getenv('PI_MAC')
TANK_MAC = os.getenv('TANK_MAC')
TP_MAC = os.getenv('TP_MAC')

def main(user_str):
    user_str = user_str.lower()
    commands = user_str.split(' ')
    if 'msi' in commands:
        send_magic_packet(MSI_MAC)
    if 'pi' in commands:
        send_magic_packet(PI_MAC)
    if 'tank' in commands:
        send_magic_packet(TANK_MAC)
    if 'tp' in commands:
        send_magic_packet(TP_MAC)
    
if __file__ == '__main__':
    user_str = input('Input the computer(s) you want to wake up (MSI PI TANK TP):')
    main(user_str)