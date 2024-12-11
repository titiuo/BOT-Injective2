import asyncio
import json
import time
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
from pyinjective.composer import Composer

from urllib import request
from urllib.error import HTTPError

WEBHOOK_URL = "https://discord.com/api/webhooks/1190668063234871296/WRT80Gr0Z9zJyOfD2k5invhr8NMJmLY18thXM9mUtQkb2i8LhH2cAc9PaPLkABgBjRGI"




async def main():
    # select network: local, testnet, mainnet
    network = Network.mainnet()
    client = AsyncClient(network)
    start=55924305
    while True:
        start=start+1
        block_height = str(start)
        print(block_height)
        a=True
        while a==True:
            try:
                block = await client.get_block(block_height=block_height)
                a=False
            except:
                print("ATT")


        txs_hash = [tx.hash.upper()[2:] for tx in block.data.txs if tx.tx_msg_types == b'["/injective.wasmx.v1.MsgExecuteContractCompat"]']
        composer = Composer(network=network.string())
        
        for tx_hash in txs_hash:
            print(tx_hash)
            a=True
            while a==True:
                try:
                    transaction_response = await client.get_tx_by_hash(tx_hash=tx_hash)
                    a=False
                except:
                    print("ERR")
            json_string=transaction_response.data.messages.decode('utf-8')
            # Charger la chaîne JSON en tant que liste de dictionnaires
            msg=json.loads(json.loads(json_string)[0]["value"]["msg"])
            premiere_clee = list(msg.keys())[0]
            if premiere_clee == "create_pair":
                contrat_adress=json.loads(transaction_response.data.logs.decode('utf-8'))[0]["events"][7]["attributes"][2]["value"]
                sentence=f"Adresse du contrat :\n{contrat_adress}"
                payload = {'content': sentence}
                headers = {'Content-Type': 'application/json', 'user-agent':'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}

                req = request.Request(url=WEBHOOK_URL,data=json.dumps(payload).encode('utf-8'),headers=headers,method='POST')

                try:
                    response = request.urlopen(req)
                except :
                    print('ERROR')
                return contrat_adress
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

