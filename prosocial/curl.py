curl -X POST -H "Content-Type: application/json" -d '{"callbot_id":"15","callcenter_phone":"0366568956","customer_phone":"0387697588","customer_area":"CENTRAL","input_slots":{"name":"Nguyễn Đức Hưng","pronoun":"anh","date": "20/07/2020","location": "Vpbank Láng Hạ","hotline": "1900545415","location_detail": "Số 25 đường Phạm Văn Đồng, thành phố Hà Nội"
}}' http://127.0.0.1:5080/api/call/create

curl -X POST -H "Content-Type: application/json" -d '{"conversation_id":"20200901120308-828efc26-7dea-4360-a852-088ba34863cb"}' http://127.0.0.1:5080/api/call/callout_safe