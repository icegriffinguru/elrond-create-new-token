# ESDT create
## About
Create new ESDT using erdpy commands.

## How to
### Create PEM
First you will need to create a wallet.pem file. To do so, you need to go on the network wallet of you choice (testnet, devnet, mainnet) and create a wallet. Keep the pass mnemonic.

Then you can call the following command to generate the .pem file:

```sh
erdpy wallet derive --mnemonic wallet/devnet/devnet-wallet.pem 
```

### Running
Now you can run the script with the following arguement.
Make sure you don't have any space of special character in the TOKEN_NAME & TOKEN_TICKER. 
```sh
sh ./create-new-token.sh <NETWORK> <TOKEN_NAME> <TOKEN_TICKER>
```

Running with python:
```py
python3 create-new-token.py -net <NETWORK> -tn <TOKEN_NAME> -tt <TOKEN_TICKER>
```