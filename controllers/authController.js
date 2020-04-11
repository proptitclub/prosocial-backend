import jwt from 'jsonwebtoken';

import { secret } from '../configs';
import { auth_user_method } from '../models/accountModel';
// import {} from '../database'

class HandlerGenerator {
  login(req, res) {
    let { username, password } = req.body;
    // console.log(req.body);
    auth_user_method({ username, password }, (error, responseCallback) => {
      if (error) {
        return res.sendStatus(400).json({
          success: false,
          message: 'Authentication failed! Please check the request',
        });
      }
      // console.log(responseCallback);
      if (responseCallback.length > 0) {
        let token = jwt.sign({ username }, secret, {
          expiresIn: '24h',
        });

        return res.json({
          success: true,
          message: 'Authentication successful!',
          token,
          user: responseCallback[0].id,
        });
      } else {
        return res.json({
          success: false,
          message: 'Incorrect username or password',
        });
      }
    });
  }
  index(req, res) {
    return res.json({
      success: true,
      message: 'Index page',
      id: '',
    });
  }
}

export const authController = new HandlerGenerator();
