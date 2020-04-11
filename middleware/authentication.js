import jwt from 'jsonwebtoken';
import { secret } from '../configs';

export const checkToken = (req, res, next) => {
  let token =
    req.headers['x-access-token'] || req.headers['authorization'] || "";
  if (token.startsWith('ProProject ')) {
    token = token.slice(11, token.length);
  }
  // console.log(token)
  if (token) {
    jwt.verify(token, secret, (err, decoded) => {
      if (err) {
        return res.json({
          success: false,
          message: 'Token is not valid',
        });
      } else {
        req.decoded = decoded;
        next();
      }
    });
  } else {
    return res.json({
      success: false,
      message: 'Auth token is not supplied',
    });
  }
};
