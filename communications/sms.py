from sendsms import api

def send_test_sms():
    api.send_sms(body='I can haz txt', from_phone='+5164485556', to=['+5164744258'])
    print("sms sent")
