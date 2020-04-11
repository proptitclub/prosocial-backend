import express from 'express';

import { checkToken as authMiddleware } from '../middleware';

import { userGroupRoleController } from '../controllers/userGroupRoleController';

export const userGroupRoleRoute = express.Router();

userGroupRoleRoute
  .route('/')
  .get((req, res) => {
    userGroupRoleController.getAllUserGroup(req, res);
  })
  .post((req, res) => {
    userGroupRoleController.addNewUserGroup(req.body, res);
  })
  .patch((req, res) => {
    userGroupRoleController.editRoleUserGroup(req.body, res);
  })
  .delete((req, res) => {
    userGroupRoleController.deleteUserGroup(req.body, res);
  });
