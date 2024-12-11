import asyncio
import json
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
from private import inj_adress

import subprocess

network = Network.mainnet()
client = AsyncClient(network)

async def account_balance(address) :
    denom = "inj"
    bank_balance = await client.get_bank_balance(address=address, denom=denom)
    amount=int(str(bank_balance).replace('balance {\n  denom: "inj"\n  amount:', '').strip()[:-2].strip('"'))
    return amount

async def buy_price():
    INJ=0.05*await account_balance(inj_adress)*1e-18
    print(INJ)
    return INJ

async def main():
    INJ_value = await buy_price()

    # Lancez une autre instance du script dans un terminal différent
    subprocess.Popen("start cmd", shell=True)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())