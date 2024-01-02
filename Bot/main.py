##Import for injective
import asyncio
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
from pyinjective.transaction import Transaction
from pyinjective.wallet import PrivateKey
from pyinjective.composer import Composer

##Private key
from private import pv_key, inj_adress, WEBHOOK_URL

#Import
from time import sleep
import json
import subprocess

##Import discord
from urllib import request
from urllib.error import HTTPError


network = Network.mainnet()
client = AsyncClient(network)



##########       SCRAP       ###########

async def scrap(start):
    # select network: local, testnet, mainnet
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
                try :
                    factory=json.loads(json.loads(transaction_response.data.logs.decode('utf-8'))[0]["events"][7]["attributes"][6]["value"])["asset_infos"][1]["native_token"]["denom"][:7]
                    test=factory=="factory"
                except:
                    test=False
                sentence=f"Adresse du contrat :\n{contrat_adress}\nFactroy: {test}"
                payload = {'content': sentence}
                headers = {'Content-Type': 'application/json', 'user-agent':'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}

                req = request.Request(url=WEBHOOK_URL,data=json.dumps(payload).encode('utf-8'),headers=headers,method='POST')

                try:
                    response = request.urlopen(req)
                except :
                    print('ERROR')
                return contrat_adress,test,start+1
#################################################
            


###############       BUY       #################

async def buy(contract,qty_INJ) -> None:
    
    qty_inj = int(qty_INJ*(10**18))
    

    # initialize grpc client
    # set custom cookie location (optional) - defaults to current dir
    composer = await client.composer()
    await client.sync_timeout_height()

    # load account
    priv_key = PrivateKey.from_hex(pv_key)
    pub_key = priv_key.to_public_key()
    address = pub_key.to_address()


    # prepare tx msg
    # NOTE: COIN MUST BE SORTED IN ALPHABETICAL ORDER BY DENOMS
    funds = [
        composer.Coin(
            amount=qty_inj,
            denom="inj",
        )
    ]
    msg = composer.MsgExecuteContract(
        sender=address.to_acc_bech32(),
        contract=contract,
        msg='{"swap":{"offer_asset":{"info":{"native_token":{"denom":"inj"}},"amount":"'+str(qty_inj)+'"}}}',
        funds=funds,
    )

    i = -1
    while True:
        await client.get_account(address.to_acc_bech32())
        i += 1
        if i%1000 == 0:
            print(i)
        # build sim tx
        tx = (
            Transaction()
            .with_messages(msg)
            .with_sequence(client.get_sequence())
            .with_account_num(client.get_number())
            .with_chain_id(network.chain_id)
        )
        sim_sign_doc = tx.get_sign_doc(pub_key)
        sim_sig = priv_key.sign(sim_sign_doc.SerializeToString())
        sim_tx_raw_bytes = tx.get_tx_data(sim_sig, pub_key)

        # simulate tx
        (sim_res, success) = await client.simulate_tx(sim_tx_raw_bytes)
        if success:
            # build tx
            gas_price = 500000000
            print(sim_res.gas_info.gas_used)
            gas_limit = sim_res.gas_info.gas_used + 300000  # add 20k for gas, fee computation
            gas_fee = "{:.18f}".format((gas_price * gas_limit) / pow(10, 18)).rstrip("0")
            fee = [
                composer.Coin(
                    amount=gas_price * gas_limit,
                    denom=network.fee_denom,
                )
            ]


            # broadcast tx: send_tx_async_mode, send_tx_sync_mode, send_tx_block_mode
            tx = tx.with_gas(gas_limit).with_fee(fee).with_memo("").with_timeout_height(client.timeout_height)
            sign_doc = tx.get_sign_doc(pub_key)
            sig = priv_key.sign(sign_doc.SerializeToString())
            tx_raw_bytes = tx.get_tx_data(sig, pub_key)

            res = await client.send_tx_sync_mode(tx_raw_bytes)
            print(res.txhash)
            print("gas fee: {} INJ".format(gas_fee))
            print(f"nombre tx sim : {i}")

            ##########      Discord       ##########

            sentence=f"Achat de :{qty_INJ} INJ"
            payload = {'content': sentence}
            headers = {'Content-Type': 'application/json', 'user-agent':'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}

            req = request.Request(url=WEBHOOK_URL,data=json.dumps(payload).encode('utf-8'),headers=headers,method='POST')

            try:
                response = request.urlopen(req)
            except :
                print('ERROR')

async def account_balance(address) :
    denom = "inj"
    bank_balance = await client.get_bank_balance(address=address, denom=denom)
    amount=int(str(bank_balance).replace('balance {\n  denom: "inj"\n  amount:', '').strip()[:-2].strip('"'))
    return amount

async def buy_price():
    '''12% de tout ce que j'ai à chaque achat'''
    INJ=0.12*await account_balance(inj_adress)*1e-18
    return INJ

#################################################
            


###############       MAIN       ################

async def main() -> None:
    start=int(input("Block de départ : "))-1
    qty_INJ=await buy_price()
    a=True
    while a==True:
        contract,factory,start=await scrap(start)
        if factory==True:
            await buy(contract,qty_INJ)
    return
#################################################


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())