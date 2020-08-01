import json, config #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
# import pdb; pdb.set_trace()

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

def post_message(user_id):
    headers = {'content-type': 'application/json'}
    url = 'https://api.twitter.com/1.1/direct_messages/events/new.json'
    
    payload = {"event": 
              {"type": "message_create",
               "message_create": {
                   "target": {"recipient_id": user_id }, 
                   "message_data": {"text": config.MESSAGE} 
               }
              }
             }
    
    payload = json.dumps(payload)
    return twitter.post(url, headers=headers, data=payload)

url = "https://api.twitter.com/1.1/users/search.json" #タイムライン取得エンドポイント
page_range = range(1, 5)
search_word = "takoyaki326"

id_list = []
name_list = []
for page in page_range:
    params ={'page': page, 'q': search_word}
    res = twitter.get(url, params = params)
    
    if res.status_code == 200:
        users = res.json()
        for user in users:
            id_list.append(user["id"])
            name_list.append(user["name"])
    else:
        print("Failed: %d" % res.status_code)

send_count = 0
success_count = 0
for id in id_list:
    name = name_list[send_count]
    send_count += 1
    res = post_message(id)
    if res.status_code == 200:
        print(name + "に送信成功しました")
        success_count += 1
    else:
        print(name + "に送信できませんでした")
    if send_count == 1:
        break
        
print('送信回数： ' + str(send_count) + '送信成功回数： ' + str(success_count))
