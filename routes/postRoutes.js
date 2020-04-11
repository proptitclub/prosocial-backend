import express from 'express';
import { postController } from '../controllers';

export const postRoute = express.Router();

postRoute
  .route('/')
  .post((req, res) => {
    const post = req.body;
    console.log('AppLog', req.body);
    postController.postPost(post, res);
  })
  .patch((req, res) => {
    const id = req.body.id;
    const content = req.body.content;
    console.log('AppLog', req.body);
    postController.updatePostById(id, content, res);
  });

postRoute.get('/:groupId', (req, res) => {
  const id = req.params.groupId;
  console.log('AppLog', id);
  postController.getPostByGroup(id, res);
});

postRoute.delete('/:id', (req, res) => {
  const id = req.params.id;
  console.log('AppLog', id);
  postController.deletePostById(id, res);
});
