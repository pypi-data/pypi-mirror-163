from defichainUtils.utils import ParamType
from defichainUtils.utils import utils,CustomTxDecode
import defichainUtils.utils.chain as chain
from defichainUtils.utils import CustomTx
# from utils import ParamType
# from utils import utils,CustomTxDecode
# import utils.chain as chain
# from utils import CustomTx
from dataclasses import dataclass


VERSION = 4
SEQUENCE = 'ffffffff'
DECIMALS = 100000000
def compose(txs:list):
    '''
    List of DfTx Class objects. Can be used for output (2.) in createrawtransaction (RPC DefiChain) 
    '''
    res = []
    for tx in txs:
        res.append(tx.hex())
    return res

def createRawTransaction(input:list,output:list,shareAddress:str,locktime:int=0,replaceable:bool=False):
    '''
    For Witness Transactions and BECH32 Addresses Only!!

    input transactions is list of dictionaries and need fields: txid, vout, amount

    output list are hex endcoded transactions. 
    UTXO output is calculated automatically and amount minus fee is sent to shareAddress.
    '''
    amount = 0
    res = ''
    res = res + utils.int2hex(VERSION,'little',4)
    res = res + utils.int2hex(len(input),'little')
    # (Unspent) UTXO
    for i in input:
        res = res + utils.convert_hex(i['txid'],'big','little')
        res = res + utils.int2hex(int(i['vout']),'little',4)
        res = res + '00'
        res = res + utils.generateSequence(SEQUENCE,locktime,replaceable)
        amount = amount + float(i['amount'])
    
    res = res + utils.int2hex(len(output)+1,'little')
    # OP_RETURN Transactions
    for i,o in enumerate(output):
        # '00' is seperator between transactions
        if i > 0:
            res = res + '00'
        res = res + utils.int2hex(0,'little',8)
        res = res + utils.int2hex(int(len(o)/2),'little')
        res = res + o

    # UTXO Output
    # '00' is seperator between transactions
    rbf = 0
    if replaceable:
        rbf = 1
    
    # TODO: signrawtransaction and get number of bytes to calculate vSize.
    dummy = '00' + utils.int2hex(0,'little',8) + utils.encodeBech32AddressToHex(shareAddress) + utils.int2hex(rbf,'little',1) + utils.int2hex(locktime,'little',4)
    
    size = int(len(res+dummy)/2)
    #size = int(736/2)
    size = int(580/2)
    # Witness data is 108 Bytes; vsize is "size" plus "3 time size minus witness data" divided by four. https://en.bitcoinwiki.org/wiki/Block_weight#Detailed_example ; https://bitcointalk.org/index.php?topic=5276203.0
    vSize = size - (108 * 3 / 4)
    print(utils.int2hex(int(amount*DECIMALS - vSize),'little',8))
    outUTXO = '00' + utils.int2hex(int(amount*DECIMALS - vSize),'little',8) + utils.encodeBech32AddressToHex(shareAddress) + utils.int2hex(rbf,'little',1) + utils.int2hex(locktime,'little',4)
    return res + outUTXO

def decodeCustomTx(hex:str):
    expectedOPReturn = hex[:2]
    
    hexLengthV1=hex[2:4]
    expectedDfTxMarkerV1 = hex[4:12]

    hexLengthV2=hex[4:6]
    expectedDfTxMarkerV2 = hex[6:14]
    if expectedOPReturn != '6a':
        # TODO: Raise Error
        return {
            'error': 1,
            'msg': 'Missing key word for OP_RETURN'
        }
    if expectedDfTxMarkerV1 == utils.stringToHex('DfTx'):
        hexLength = hexLengthV1
        txLock = None
        hex = hex[4:]  
    elif expectedDfTxMarkerV2 == utils.stringToHex('DfTx'):
        hexLength = hexLengthV2
        txLock = hex[2:4]
        hex = hex[6:] 
    else:
        # TODO: Raise Error
        return {
            'error': 1,
            'msg': 'Missing key word for DfTx marker'
        }

    if int(hexLength,16) != int(len(hex)/2):
        # TODO: Raise Error
        return {
            'error': 1,
            'msg': 'Indicated length in hex string does fit string length'
        }
    return CustomTxDecode.decodeCustomTx(hex[8:])

def processCustomTransactionOnChain(block,name,parameters:dict,pool:dict):
    '''
    block: blockHeight
    name: Name of the rpc function (lowercase), e.g. poolswap (compositeswap is a chain of poolswaps!!! Act accordingly. Only poolswap possible)
    pool: pool keys with value - "reserveA", "reserveB", "totalLiquidity", "poolSymbol" (e.g. TSLA-DUSD)
    parameters: function keys with value - 
        - addpoolliquidity: "amountA", "amountB" (amount of Tokens; must be in correct order depending on poolpair. E.g. TSLA-DUSD means amountA is TSLA Amount)
        - removePoolLiquidity: "liquidity" (amount of Poolpair Tokens)
        - poolSwap: "tokenFrom", "fromAmount", "commission", "dexFeeInPct"
    
    RETURN:
    addpoolliquidity: amount liquidity tokens
    removepoolliquidity: amount of TokenA and TokenB (tuple) ->
    poolswap: amount of new reserveFrom, new reserveTo and amount TokenTo (tuple)
    '''
    if 'reserveA' not in pool or 'reserveB' not in pool:
        # TODO: Raise Error
        return {
            'error': 1,
            'msg': 'reserveA and/or reserveB missing'
        }
    if name == 'addpoolliquidity':
        if 'amountA' not in parameters or 'amountB' not in parameters or 'totalLiquidity' not in pool:
            # TODO: Raise Error
            return {
                'error': 1,
                'msg': 'amountA and/or amountB and/or totalLiquidity missing'
            } 
        liquidity = chain.addPoolLiquidity(parameters['amountA'],parameters['amountB'],pool['reserveA'],pool['reserveB'],pool['totalLiquidity'])
        return {
            'success': 1,
            'liquidity': liquidity
        }
    elif name == 'removepoolliquidity':
        if 'liquidity' not in parameters or 'totalLiquidity' not in pool:
            # TODO: Raise Error
            return {
                'error': 1,
                'msg': 'liquidity and/or totalLiquidity missing'
            } 
        (amountA,amountB) = chain.removePoolLiquidity(parameters['liquidity'],pool['reserveA'],pool['reserveB'],pool['totalLiquidity'])
        return {
            'success': 1,
            'amountA': amountA,
            'amountB': amountB
        }
    elif name == 'poolswap':
        if 'tokenFrom' not in parameters or 'fromAmount' not in parameters or 'symbol' not in pool or 'commission' not in parameters or 'dexFeeInPct' not in parameters:
            # TODO: Raise Error
            return {
                'error': 1,
                'msg': 'tokenFrom and/or fromAmount and/or symbol and/or commission and/or dexFeeInPct missing'
            } 
        (poolFrom,poolTo,swapped) = chain.poolSwap(block,parameters['tokenFrom'],pool['symbol'],parameters['fromAmount'],pool['reserveA'],pool['reserveB'],parameters['commission'],parameters['dexFeeInPct'])
        return {
            'success': 1,
            'reserveFrom': poolFrom,
            'reserveTo': poolTo,
            'swapped': swapped
        }

# TODO: only working in python3.9 not in 3.8!!!
# class TakeLoan(CustomTx.DfTx):
#     def __init__(self,vaultId:str,address:str,amounts:list,rpcConnector):
#         super().__init__()
#         resAmounts = []
#         for a in amounts:
#             amount = a.split('@')
#             resAmounts.append((float(amount[0]),utils.getTokenId(amount[1],rpcConnector)))
#         self.params = [CustomTx.CustomTxType.TakeLoan,ParamType.Vault(vaultId),ParamType.Address(address),ParamType.Amounts(resAmounts)]

# class AddPoolLiquidity(CustomTx.DfTx):
#     def __init__(self,amountPerAddress:list[tuple[str,str]],shareAddress:str,rpcConnector):
#         super().__init__()
#         resAddressAmount = []
#         for a in amountPerAddress:
#             amount = a[1].split('@')
#             resAddressAmount.append((a[0],float(amount[0]),utils.getTokenId(amount[1],rpcConnector)))
#         self.params = [CustomTx.CustomTxType.AddPoolLiquidity,ParamType.AddressesWithAmount(resAddressAmount),ParamType.Address(shareAddress)]

@dataclass
class RPCConnector():
    NODE_URL:str
    NODE_USER:str
    NODE_PASSWORD:str


# if __name__ == '__main__':
#     #a = 'df1qamj6pp30h9y3syqcz8nwnekzg8dswul3tw5kjy'
#     #adr = utils.encodeBech32AddressToHex(a)

#     hex ='6a4c4d446654786c01160014f0d78fb00b5a3dfcf3e872e27c6ec5f97005e5d7026a000000a05a3200000000000f000000d718810400000000160014f0d78fb00b5a3dfcf3e872e27c6ec5f97005e5d7'
#     #hex = '6a4c4f4466547869160014eee5a0862fb94918101811e6e9e6c241db0773f1000a00000000000000160014eee5a0862fb94918101811e6e9e6c241db0773f102ffffffffffffff7fffffffffffffff7f0105'
#     print(decodeCustomTx(hex))
    
    # print(hex(2059200))
    #print(utils.int2hex(144015528,'little',8))
    # #print(int(utils.convert_hex('b95f2f0300000000','little','big'),16)/100000000)
    # print(int(utils.convert_hex('90eac90100000000','big','little'),16))
    

    # # This is how this package could be used.
    # v = 'ed299afd57b7b354983efce9254436c7409e2c52a152d0a41bec0fb477f3a0b6'
    # a = 'tf1q6qj52ykxlf6halmx0g32gaumuuptactwgrqh23'

    # # a = 'df1q6qcutr37ex6xd5mjcmgrlr9239ck9z22605hfp'

    # RPCConn =RPCConnector("","","")
    # t = TakeLoan(v,a,["0.00112715@MSFT","1@DUSD"],RPCConn)
    # #print(t.hex())
    # p = AddPoolLiquidity([(a,"1@DUSD"),(a,"0.00112715@MSFT")],a,RPCConn)

    # input = {
    #     "txid":"b8639f6f27318c281f574ecb0360c1340e91e32780ca8da5c621a64a24026739",
    #     "vout":1,
    #     "amount":0.91485041
    # }
    # print(createRawTransaction([input],[t.hex()],a))
    # # print(t.hex())
    # # #d = DfTx(cTxType.TakeLoan,[v,a])
    # # #print(d.getHex())

    
