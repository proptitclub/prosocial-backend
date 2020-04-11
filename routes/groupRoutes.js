import express from 'express';
import { groupController } from '../controllers';

export const groupRoute = express.Router();

groupRoute
  .route('/')
  .get((req, res) => {
    groupController.getAllGroups(req, res);
  })
  .post((req, res) => {
    groupController.addNewGroup(req.body, res);
  })
  .patch((req, res) => {
    groupController.editGroup(req.body, res);
  })
  .delete((req, res) => {
    groupController.deleteGroup(req.body, res);
  });

groupRoute.get('/:id', (req, res) => {
  groupController.getGroupById(req.params.id, res);
});
