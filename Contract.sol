pragma solidity ^0.4.0;
contract Contract
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
            //console.log("new visited, hospitalId - " + hospitalId + ", patientId - " + msg.sender);
            patients[msg.sender].isVisited[hospitalId] = true;
            keyIndex = patients[msg.sender].keys.length++;
            patients[msg.sender].keys[keyIndex] = hospitalId;
        }
    }

    function isPermissioned(address hospitalId, address patientId) view public returns (bool) {
        //console.log("I'm allowed!!");
        return (permissionsTime[patientId][hospitalId] >= now);
    }

    function AmIPermissioned(address patientId) view public returns (bool) {
        return isPermissioned(msg.sender, patientId);
    }

    function whereVisited(address patientId) view public returns (address[]) {
        if (AmIPermissioned(patientId)) //If I'm allowed.
        {
            
            return patients[patientId].keys;
        }
        address[] storage empty;
        return empty;
    }

    function addPatient(string name) public{
        if(patients[msg.sender].isExist == false){
            //console.log("added patient - " + name + "\n");
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
 
