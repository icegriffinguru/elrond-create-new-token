##### - configuration - #####
NETWORK_NAME="testnet" # devnet, testnet, mainnet
PROXY=https://testnet-gateway.elrond.com
CHAIN_ID="T"

ESDT_ISSUE_ADDRESS=erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u
DEPLOYER="./wallet/testnet/testnet-wallet.pem" # main actor pem file

TOKEN_NAME="Sven"
TOKEN_TICKER="SVEN"

TOKEN_NAME_HEX="$(echo -n ${TOKEN_NAME} | xxd -p -u | tr -d '\n')"
TOKEN_TICKER_HEX="$(echo -n ${TOKEN_TICKER} | xxd -p -u | tr -d '\n')"

# https://docs.elrond.com/developers/esdt-tokens/#issuance-of-fungible-esdt-tokens
# initial supply: 1e24 wei - 1e6 $ESDT
# number of decimals: 18
DATA="issue@${TOKEN_NAME_HEX}@${TOKEN_TICKER_HEX}@d3c21bcecceda1000000@12@63616e467265657a65@74727565@63616e57697065@74727565@63616e5061757365@74727565@63616e4d696e74@74727565@63616e4275726e@74727565@63616e55706772616465@74727565"

ADDRESS=$(erdpy data load --partition ${NETWORK_NAME} --key=address)
DEPLOY_TRANSACTION=$(erdpy data load --partition ${NETWORK_NAME} --key=deploy-transaction)

echo "TEST A $1";

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

"$@"