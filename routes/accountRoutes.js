import express from 'express';
import { accountController } from '../controllers';
import { checkToken as authMiddleware } from '../middleware';

export const accountRoute = express.Router();

accountRoute
  .route('/')
  .get((req, res) => {
    accountController.getAllUsers(req, res);
  })
  .post((req, res) => {
    accountController.addNewUser(req.body, res);
  })
  .patch((req, res) => {
    accountController.editUser(req.body, res);
  })
  .delete((req, res) => {
    accountController.deleteUser(req.body, res);
  });

accountRoute.get('/:id', (req, res) => {
  accountController.getUserById(req.params.id, res);
});
