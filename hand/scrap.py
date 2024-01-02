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
    block_height = "55912074"
    a=True
    while a==True:
        try:
            block = await client.get_block(block_height=block_height)
            a=False
        except:
            print()
            print()
            print("ATTENTE DU BLOCK")
            print()
            print()
            time.sleep(1)
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
            print(contrat_adress)
    
    
    ### si vous voulez tester sur le choix d'un block ###
    #block_height = "55327294"
    #block = await client.get_block(block_height=block_height) 
    #inj14gus8a0zuhm30mwsxz2puu868n8ke7gvtcylvn
    #{'type': '/injective.wasmx.v1.MsgExecuteContractCompat', 'value': {'sender': 'inj1n25arfnh9th57esvddur89lq8ucc2x85dk33ss', 'contract': 'inj13ef32swyqexktt8km80wsegdpd57zls55w3q0e', 'msg': '{"swap":{"offer_asset":{"info":{"native_token":{"denom":"inj"}},"amount":"100000000000000000"},"max_spread":"0.5","belief_price":"50.136986489995146361"}}', 'funds': '100000000000000000inj'}}7DCC5502C67B674CE15050637944BD00194693F2DB5C1D791E1D3E4873F56B88
    #[{"type":"/injective.wasmx.v1.MsgExecuteContractCompat","value":{"sender":"inj1h4usvhhva6dgmun9rk4haeh8lynln7yhk6ym00","contract":"inj19aenkaj6qhymmt746av8ck4r8euthq3zmxr2r6","msg":"{\\"create_pair\\":{\\"pair_type\\":{\\"xyk\\":{}},\\"asset_infos\\":[{\\"native_token\\":{\\"denom\\":\\"factory/inj1h4usvhhva6dgmun9rk4haeh8lynln7yhk6ym00/PIKA\\"}},{\\"native_token\\":{\\"denom\\":\\"inj\\"}}],\\"init_params\\":\\"e30=\\"}}","funds":"0"}}]'
    #<grpc.aio.EOF>

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())