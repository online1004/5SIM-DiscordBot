import requests

def req_buy(product, country):
    token = ''
    operator = 'any'

    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
    }
    response = requests.get('https://5sim.net/v1/user/buy/activation/' + country + '/' + operator + '/' + product, headers=headers)
    return response.json()

def req_order(id):
    token = ''

    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
    }
    response = requests.get('https://5sim.net/v1/user/check/' + id, headers=headers)
    data = response.json()
    if data['status'] == 'RECEIVED':
        try:
            return data['sms'][0]['code']
        except IndexError:
            return 'FAIL'
    elif data['status'] == 'TIMEOUT':
        return 'TIMEOUT'
    elif data['status'] == 'BANNED':
        return 'BANNED'
    return 'FAIL'