# """
# 1. get transactions list for 'getAddressHistory/' - each transaction
# have 2 records (epic > eth, eth > epic)
# 2. get tx id and paste to 'getTxInfo/'
# 3. if eth > epic transaction:
#
#      ['operations']['0']['usdPrice'] * ['operations']['0']['intvalue']
#      eth_price * eth_amount = tx_value (in usd)
#
#      ['operations']['1']['intvalue'] = epic_amount
#      tx_value / epic_amount = epic_price (in usd)
#
#    if epic > eth transaction:
# """
#
#
# def uniswap_data():
#
# queries = {
#     'address': 'getAddressInfo/',
#     'operations': 'getAddressHistory/',
#     'tx': 'getTxInfo/',
#     }
# address = '0xc27908ed2f80dd8a799625114730f9f10cf89d94'
# target = 'eth'
# exchange = Exchange.objects.get(name='Uniswap')
# coin = Coin.objects.get(symbol="EPIC")
#
# def uniswap_api(query, address, breaks=False):
#     key = '?apiKey=' + uniswap_key
#     url = "https://api.ethplorer.io/" + query + address + key
#     return json.loads(requests.get(url).content)
#
# tx_data = {}
#
# for operation in uniswap_api(query=queries['operations'], address=address)['operations'][:2]:
#     if operation['tokenInfo']['symbol'] == 'EPIC':
#         tx_data.update({'epic_amount': int(operation['value'])/1000000000000000000})
#     elif operation['tokenInfo']['symbol'] == 'WETH':
#         for op in uniswap_api(query=queries['tx'],
#             address=operation['transactionHash'])['operations']:
#                 if op['tokenInfo']['price']:
#                     tx_data.update({
#                         'value': (int(operation['value']) / 1000000000000000000) * float(op['usdPrice'])})
#
#
#
#
#
#
# # tx_data = {
# #     op['timestamp']: {
# #         uniswap_api(query=queries['tx'], address=op['transactionHash'])['operations']['0']['usdPrice']
# #          }
# #     for op in uniswap_api(query=queries['operations'], address=address)['operations']
# #     }
#


