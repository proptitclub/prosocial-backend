import uuid from 'uuid';

import {
  patch_user_method,
  get_users_method,
  post_user_method,
  delete_user_method,
  auth_user_method,
} from '../models/accountModel';

class Account {
  constructor() {
    this.table = 'users';
    this.accounts = [];
  }

  getAllUsers(req, res) {
    get_users_method(null, (err, users) => {
      if (err) res.send(err);
      else {
        this.accounts = users;
        res.send(this.accounts);
      }
    });
  }

  getUserById(userId, res) {
    get_users_method(userId, (err, users) => {
      if (err) res.send(err);
      else res.send(users[0]);
    });
  }

  editUser(user, res) {
    patch_user_method(user, err => {
      if (err) console.log(err);
      else res.send('Patch successfully');
    });
    // this.accounts = this.accounts.map(account => {
    //   if (account.id === user.id) {
    //     return user;
    //   } else return account;
    // });
    // return this.accounts;
  }

  addNewUser(user, res) {
    console.log(user.username);
    auth_user_method(
      {
        username: user.username,
      },
      (err, response) => {
        if (err) {
          console.log(err);
        } else {
          console.log(response);
          if (response.length > 0) {
            res.json({
              success: false,
              message: 'Username was existed',
            });
          } else {
            post_user_method(
              {
                id: uuid(),
                user,
              },
              (err, response) => {
                if (err) console.log(err);
                else
                  res.json({
                    success: true,
                    message: 'Create user successfully',
                  });
              },
            );
          }
        }
      },
    );
  }

  deleteUser(body, res) {
    delete_user_method(body.id, err => {
      if (err) console.log(err);
      else res.send('Delete Account Successful');
    });
  }
}

export const accountController = new Account();
