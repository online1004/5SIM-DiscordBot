import requests 

def toss_request(toss_id:str, amount:str):
    try:
        header = {"token" : ""}
        json = {"id": toss_id, "amount": amount}
        res = requests.post('http://127.0.0.1:443/api/toss/request', headers=header, json=json)
        post_json = res.json()
        if post_json['result'] == 'FAIL':
            print (post_json['message'])
            return 'FAIL'
        name = post_json['code']
        acc = post_json['accNumber']
        return name, acc
    except Exception as e:
        print(e)
        return 'FAIL'
    
def toss_confirm(code:str):
    header = {"token" : ""}
    json = {"code": code}
    res = requests.post('http://127.0.0.1:443/api/toss/confirm', json=json, headers=header)
    post_json = res.json()
    result = post_json['result']
    message = post_json['message']
    return result, message
