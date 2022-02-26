##### - configuration - #####
NETWORK_NAME="$1" # devnet, testnet, mainnet

if [ $NETWORK_NAME = "devnet" ]; then
    CHAIN_ID="D"
elif [ $NETWORK_NAME = "testnet" ]; then
    CHAIN_ID="T"
elif [ $NETWORK_NAME = "mainnet" ]; then
    CHAIN_ID="1"
else
    echo "Wrong NETWORK name, please choose betwee: devnet, testnet, mainnet !"
    exit
fi
PROXY="https://${NETWORK_NAME}-gateway.elrond.com"
DEPLOYER="./wallet/${NETWORK_NAME}/${NETWORK_NAME}-wallet.pem" # main actor pem file

ESDT_ISSUE_ADDRESS=erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u

TOKEN_NAME="$2"
TOKEN_TICKER="$3"

TOKEN_NAME_HEX="$(echo "${TOKEN_NAME}" | xxd -p)"
TOKEN_TICKER_HEX="$(echo "${TOKEN_TICKER}" | xxd -p)"

# https://docs.elrond.com/developers/esdt-tokens/#issuance-of-fungible-esdt-tokens
# initial supply: 1e24 wei - 1e6 $ESDT
# number of decimals: 18
DATA="issue@${TOKEN_NAME_HEX}@${TOKEN_TICKER_HEX}@d3c21bcecceda1000000@12@63616e467265657a65@74727565@63616e57697065@74727565@63616e5061757365@74727565@63616e4d696e74@74727565@63616e4275726e@74727565@63616e55706772616465@74727565"

ADDRESS=$(erdpy data load --partition ${NETWORK_NAME} --key=address)
DEPLOY_TRANSACTION=$(erdpy data load --partition ${NETWORK_NAME} --key=deploy-transaction)

issue_token() {
    echo "issuing token to ${NETWORK_NAME} ...";
    erdpy --verbose tx new \
        --recall-nonce \
        --pem=${DEPLOYER} \
        --gas-limit=500000000 \
        --outfile="deploy-${NETWORK_NAME}.interaction.json" \
        --proxy=${PROXY} \
        --chain=${CHAIN_ID} \
        --value 50000000000000000 \
        --receiver ${ESDT_ISSUE_ADDRESS} \
        --data="${DATA}" \
        --send || return
}

echo "Create EDST: ($1, $2)";

issue_token
