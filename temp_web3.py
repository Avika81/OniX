import json
import web3
import os

from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.0;
contract TestContract
{
    struct patient{
        address id;
        string name;
        mapping(address=>bool) isVisited;
        address[] keys;
        bool isExist;
    }


    mapping(address=>patient) patients;
    mapping(address=>mapping(address=>uint)) permissionsTime;
    //first address is patient,
    //second is hospital, the uid is the endTime

    function approveHospitalUntil(address hospitalId, uint endTime) public{
        permissionsTime[msg.sender][hospitalId] = endTime;
    }

    function hospitalVisited(address hospitalId) public{
        uint keyIndex;
        if(!patients[msg.sender].isVisited[hospitalId]){
            patients[msg.sender].isVisited[hospitalId] = true;
            keyIndex = patients[msg.sender].keys.length++;
            patients[msg.sender].keys[keyIndex] = hospitalId;
        }
    }

    function isPermissioned(address hospitalId, address patientId) view public returns (bool) {
        return (permissionsTime[patientId][hospitalId] >= now); //is working????????????????????????
    }

    function AmIPermissioned(address patientId) view public returns (bool) {
        return isPermissioned(msg.sender, patientId);
    }

    function whereVisited(address patientId) view public returns (address[]) {
        if (AmIPermissioned(patientId)) //If I'm allowed0
        {
            return patients[patientId].keys; //NEED TO CHECK IF THIS IS A HARD COPY OR NOT
        }
        address[] storage empty;
        return empty;
    }

    function addPatient(string name) public{
        if(patients[msg.sender].isExist == false){
            patient storage newPatient;
            newPatient.id = msg.sender;
            newPatient.name = name;
            newPatient.isExist = true;
            patients[msg.sender] = newPatient;
        }
    }

    function getMyName() view public returns (string){
        return patients[msg.sender].name;
    }
}
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:TestContract']

# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://bchrnv-dns-reg1.westeurope.cloudapp.azure.com:8545"))
# Instantiate and deploy contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 410000})

# Get tx receipt to get contract address
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
contract_address = tx_receipt.contractAddress
contract_instance = w3.eth.contract(address=contract_address, abi=abi,ContractFactoryClass=ConciseContract)

# Contract instance in concise mode
abi = contract_interface['abi']
contract_instance = w3.eth.contract(address=contract_address, abi=abi,ContractFactoryClass=ConciseContract)
