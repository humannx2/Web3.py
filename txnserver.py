from flask import Flask,request,jsonify
from web3 import Web3

app=Flask(__name__)

con=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545')) #ganache url

@app.route('/')
def home():
    print(con.is_connected())
    return 'con'

@app.route('/txn', methods=['POST'])
def txn():
    # use json to get raw data from the front end
    acc1=request.json.get('sender')
    acc2=request.json.get('receiver')
    amt=request.json.get('amount')
    pvt_key=request.json.get('key')

    if not con.is_address(acc1) or not con.is_address(acc2):
        return jsonify({'error':'Invalid Sender or Receiver Address.'}),400 #changes the status code to 400, bad request

    balance=con.eth.get_balance(acc1)
    if balance<amt:
        return jsonify({'error':'Insufficient Funds'}),400

    #creating the transaction

    nonce=con.eth.get_transaction_count(acc1)  #keeps count of txn and prevent multiple txns
    txn={
        'nonce':nonce,
        'to':acc2,
        'value':con.to_wei(amt,'ether'),
        'gas':200000,
        'gasPrice': con.to_wei('100','gwei')
    }
    #  signing txn
    signtxn=con.eth.account.sign_transaction(txn,pvt_key)
    # sending txn
    txh_hash=con.eth.send_raw_transaction(signtxn.rawTransaction)
    txn_hex=con.to_hex(txh_hash)
    return jsonify({'Transaction Hex':txn_hex}),200

if __name__=='__main__':
    app.run(debug=True)