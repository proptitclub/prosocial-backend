import {
  get_user_group_method,
  patch_user_group_method,
  delete_user_group_method,
} from '../models/userGroupRoleModel';

import { tbl_UGR } from '../helpers';

class UserGroupRole {
  constructor() {
    this.table = tbl_UGR;
    this.userGroup = [];
  }

  getAllUserGroup(req, res) {
    get_user_group_method(null, (err, result) => {
      if (err) {
        return res.json({
          success: false,
          message: 'Error',
        });
      } else {
        this.userGroup = result;
        return res.send(this.userGroup);
      }
    });
  }

  editRoleUserGroup(req, res) {
    patch_user_group_method(req, err => {
      if (err) {
        return res.json({
          success: false,
          message: 'Error',
        });
      } else {
        return res.json({
          success: true,
          message: 'Edit role user successfully',
        });
      }
    });
  }

  addNewUserGroup(req, res) {
    post_user_method(req, (err, result) => {
      if (err) {
        return res.json({
          success: false,
          message: 'Error',
        });
      } else {
        return res.json({
          success: true,
          message: 'Create user group successfully',
        });
      }
    });
  }

  deleteUserGroup(req, res) {
    delete_user_group_method(req, err => {
      if (err) {
        return res.json({
          success: false,
          message: 'Error',
        });
      } else {
        return res.json({
          success: true,
          message: 'Delete user group successfully',
        });
      }
    });
  }
}

export const userGroupRoleController = new UserGroupRole();
