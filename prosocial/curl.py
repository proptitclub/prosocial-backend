curl -X POST -H "Content-Type: application/json" -d '{"callbot_id":"15","callcenter_phone":"0366568956","customer_phone":"0387697588","customer_area":"CENTRAL","input_slots":{"name":"NGUYEN VAN HAI","pronoun":"anh","date": "20/07/2020","location": "Vpbank Láng Hạ","hotline": "1900545415","location_detail": "Số 25 đường Phạm Văn Đồng, thành phố Hà Nội"
}}' http://127.0.0.1:5080/api/call/create

curl -X POST -H "Content-Type: application/json" -d '{"conversation_id":"20200909105923-7d846cd6-2d2b-4ce5-b04c-4d712db28933"}' http://127.0.0.1:5080/api/call/callout_safe