# django_jwt
- cách lấy token: POST request vào url "/api-auth/token/obtain/" kèm theo header có chứa "Content-Type: application/json",
POST request bao gồm body gồm có "username" và "password"
- token trả về gồm 2 phần: một là "access", token này tồn tại 5 phút, hai là "refresh" tồn tại trong 1 ngày
- khi access hết hạn thì request vào url "/api-auth/token/refresh/" kèm theo header có chứa "Content-Type: application/json", POST request bao gồm body có "refresh" token, nó sẽ trả về "access" token để tiếp tục sử dụng
- khi request vào một url yêu cầu authentication thì kèm theo header có chứa "Authorization: Bearer {}".format(access_token)
