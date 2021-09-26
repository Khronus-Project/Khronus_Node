from khron_node.khron_services.web3_service import get_node_contract, fulfill_alert, getPublicKey, estimateAlertGas

def testTransaction(alertID):
    contract = get_node_contract()
    print(type(alertID))
    print(alertID)
    txt = fulfill_alert(contract, alertID)
    print(txt)
    
def estimate_gas(alertID):
    contract = get_node_contract()
    return estimateAlertGas(contract, alertID)

def whatKey():
    return getPublicKey()
