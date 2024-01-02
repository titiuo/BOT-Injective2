import asyncio
import json
import time
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
from pyinjective.composer import Composer




async def main() -> None:
    # select network: local, testnet, mainnet
    network = Network.mainnet()
    client = AsyncClient(network)
    start=56130845
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
                print("...")


        txs_hash = [tx.hash.upper()[2:] for tx in block.data.txs if tx.tx_msg_types == b'["/injective.wasmx.v1.MsgExecuteContractCompat"]']
        composer = Composer(network=network.string())
        
        for tx_hash in txs_hash:
            transaction_response = await client.get_tx_by_hash(tx_hash=tx_hash)
            json_string=transaction_response.data.messages.decode('utf-8')
            # Charger la chaîne JSON en tant que liste de dictionnaires
            msg=json.loads(json.loads(json_string)[0]["value"]["msg"])
            premiere_clee = list(msg.keys())[0]
            if premiere_clee == "create_pair":
                contrat_adress=json.loads(transaction_response.data.logs.decode('utf-8'))[0]["events"][7]["attributes"][2]["value"]
                factory=json.loads(json.loads(transaction_response.data.logs.decode('utf-8'))[0]["events"][7]["attributes"][6]["value"])["asset_infos"][1]["native_token"]["denom"]
                print(contrat_adress)
                print(factory[:7]=="factory")
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())