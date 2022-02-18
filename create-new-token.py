import requests
import subprocess
import ast
import json
import time


OWNER_PEMFILE = "./wallet/testnet/testnet-wallet.pem"
PROXY_URL = "https://testnet-api.elrond.com"
GATEWAY_URL = "https://testnet-gateway.elrond.com"

# OWNER_PEMFILE = "./wallet/devnet/devnet-wallet.pem"
# PROXY_URL = "https://devnet-api.elrond.com"
# GATEWAY_URL = "https://devnet-gateway.elrond.com"

ESDT_ISSUE_ADDRESS = "erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u"


## token ticker rule:
#   - length limit ?
#   - only contain capital letters?

## extra "data params" - you can add these parmas to data
# Smart: @canFreeze@true@canWipe@true@canPause@true@canMint@true@canBurn@true@canUpgrade@true
# Raw: @63616e467265657a65@74727565@63616e57697065@74727565@63616e5061757365@74727565@63616e4d696e74@74727565@63616e4275726e@74727565@63616e55706772616465@74727565

def IssueTokenTransaction():
    data = "issue"
    data += "@536e6f77466c616b65"   # token name: "SnowFlake"
    data += "@534643"               # token ticker: "SFC"
    data += "@d3c21bcecceda1000000" # initial supply: 1e24 wei - 1e6 $ESDT
    data += "@12"                   # number of decimals: 18
    data += "@63616e467265657a65@74727565@63616e57697065@74727565@63616e5061757365@74727565@63616e4d696e74@74727565@63616e4275726e@74727565@63616e55706772616465@74727565"

    command = "erdpy tx new "
    command += " --pem=\"{0}\" ".format(OWNER_PEMFILE)
    command += " --proxy=\"{0}\" ".format(PROXY_URL)
    command += " --data=\"{0}\" ".format(data)

    command += " --receiver {0} ".format(ESDT_ISSUE_ADDRESS)
    command += " --value {0} ".format(50000000000000000)
    command += " --gas-limit {0} ".format(60000000)

    command += "--recall-nonce "
    command += " --send "

    # print("Command: {0}".format(command))

    process = subprocess.run(command, shell = True, stdout = subprocess.PIPE)
    json_tx = process.stdout

    # print("json_tx: {0}".format(json_tx))
    
    return json_tx


def GetTransactionStatus():
    query = GATEWAY_URL + "/transaction/" + hash_value + "/status?withResults=true"
    request = requests.get(query)
    
    return request


def main():
    tx_output = IssueTokenTransaction()
    print()
    
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
    main()