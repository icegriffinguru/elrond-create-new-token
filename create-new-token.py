import requests
import subprocess
import ast
import json
import time
import argparse


ESDT_ISSUE_ADDRESS = "erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u"


## token ticker rule:
#   - length limit ?
#   - only contain capital letters?

## extra "data params" - you can add these parmas to data
# Smart: @canFreeze@true@canWipe@true@canPause@true@canMint@true@canBurn@true@canUpgrade@true
# Raw: @63616e467265657a65@74727565@63616e57697065@74727565@63616e5061757365@74727565@63616e4d696e74@74727565@63616e4275726e@74727565@63616e55706772616465@74727565

def IssueTokenTransaction(name, ticker):
    data = "issue"
    data += f"@{name.encode('utf-8').hex()}"    # token name
    data += f"@{ticker.upper().encode('utf-8').hex()}"  # token ticker
    data += "@d3c21bcecceda1000000"             # initial supply: 1e24 wei - 1e6 $ESDT
    data += "@12"                               # number of decimals: 18
    data += "@63616e467265657a65@74727565@63616e57697065@74727565@63616e5061757365@74727565@63616e4d696e74@74727565@63616e4275726e@74727565@63616e55706772616465@74727565"

    command = "erdpy tx new "
    command += " --pem=\"{0}\" ".format(OWNER_PEMFILE)
    command += " --proxy=\"{0}\" ".format(PROXY_URL)
    command += " --chain=\"{0}\" ".format(CHAIN_ID)
    command += " --data=\"{0}\" ".format(data)

    command += " --receiver {0} ".format(ESDT_ISSUE_ADDRESS)
    command += " --value {0} ".format(50000000000000000)
    command += " --gas-limit {0} ".format(60000000)

    command += "--recall-nonce "
    command += " --send "


    process = subprocess.run(command, shell = True, stdout = subprocess.PIPE)
    json_tx = process.stdout
    return json_tx


def GetTransactionStatus():
    query = GATEWAY_URL + "/transaction/" + hash_value + "/status?withResults=true"
    request = requests.get(query)

    return request

def _pick_chain_id(network):
    if network == 'devnet': return 'D'
    if network == 'testnet': return 'T'
    if network == 'mainnet': return '1'
    print('Error wrong ntwork name (devnet, testnet, mainnet).')

def main(token_name, token_ticker):
    tx_output = IssueTokenTransaction(token_name, token_ticker)

    tx_output = tx_output.decode("UTF-8")
    tx_dict = ast.literal_eval(tx_output)
    global hash_value
    hash_value = tx_dict["hash"]

    # waiting for the end of the transaction
    wait_seconds = 20
    print("Waiting for {0} seconds...".format(wait_seconds))
    time.sleep(wait_seconds)

    req = GetTransactionStatus()
    req_dict = json.loads(req.text)

    print("IssueTokenTransaction status : ", req_dict.get("data", {}).get("status"))
    print("Status: {0}".format(req_dict))

    # In elrond explorer, you can see token identifier on "Logs" tab's "Topics" input field.
    # i.e. "SFC-55ba74"

if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    # Adding optional argument
    parser.add_argument("-net", "--network", help="Network name (mainnet, devnet, testnet)")
    # See here for the format:
    # https://docs.elrond.com/developers/esdt-tokens/#parameters-format
    parser.add_argument("-tn", "--tokenname", help="Token name (no special characters or spaces in it)")
    parser.add_argument("-tt", "--tokenticker", help="Token ticker (no special characters or spaces in it)")
    # Read arguments from command line
    args = parser.parse_args()

    OWNER_PEMFILE = f"./wallet/{args.network}/{args.network}-wallet.pem"
    PROXY_URL = f"https://{args.network}-api.elrond.com"
    subdomain_gateway = args.network+'-' if args.network != 'mainnet' else ''

    GATEWAY_URL = f"https://{subdomain_gateway}gateway.elrond.com"
    CHAIN_ID = _pick_chain_id(args.network)

    main(args.tokenname, args.tokenticker)
