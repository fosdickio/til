# Web3.js Notes

## Introducton

- Ethereum nodes communicate using JSON-RPC
- Web3.js provides a convenient and easily readable JavaScript interface

```bash
yarn add web3
```

## Web3 Providers

- Ethereum is made up of nodes that all share a copy of the same data
- Setting a Web3 Provider in Web3.js tells our code which node we should be talking to handle our reads and writes

## Talking to Contracts

### Contract Address

- After you deploy your contract, it gets a fixed address on Ethereum where it will live forever
- You'll need to copy this address after deploying in order to talk to your smart contract

### Contract ABI

- The other thing Web3.js will need to talk to your contract is its ABI
- ABI stands for Application Binary Interface
- The ABI is essentially a representation of your contracts' methods in JSON format that tells Web3.js how to format function calls in a way your contract will understand

## Calling Contract Functions

- In Solidity, when you declare a variable `public`, it automatically creates a `public` "getter" function with the same name

### Call

- `call` is used for `view` and `pure` functions
  - `view` and `pure` functions are read-only and don't change state on the blockchain
  - They also don't cost any gas and the user won't be prompted to sign a transaction with MetaMask
- It only runs on the local node and won't create a transaction on the blockchain

Using Web3.js, you would call a function named `myMethod` with the parameter `123` as follows:

```javascript
myContract.methods.myMethod(123).call();
```

### Send

- `send` will create a transaction and change data on the blockchain
  - Sending a transaction will require the user to pay gas and will pop up their Metamask to prompt them to sign a transaction.
- You'll need to use send for any functions that aren't `view` or `pure`

Using Web3.js, you would send a transaction calling a function named `myMethod` with the parameter `123` as follows:

```javascript
myContract.methods.myMethod(123).send();
```
