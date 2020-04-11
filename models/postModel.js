import { connection } from '../database';

const POSTS_TABLE = `posts`;

export const post_post_method = (
  { id, userId, groupId, content, type = 1 } = post,
  result,
) => {
  const sql = `INSERT INTO ${POSTS_TABLE}(id, userId, groupId, content, type) 
                VALUES ('${id}', '${userId}', '${groupId}', '${content}', '${type}')`;
  connection.query(sql, (err, res) => {
    if (err) {
      console.log('AppLog', err);
    } else {
      result(res);
    }
  });
};

/**
 * get all post from database
 */

export const get_all_posts_method = (groupId, result) => {
  const sql = `SELECT posts.id, posts.groupId, posts.content, posts.time, posts.type, posts.userId AS authorId, reactions.userId AS reactuserId, comments.id AS commentId FROM posts LEFT OUTER JOIN reactions ON groupId = '${groupId}' AND posts.id = reactions.postId LEFT OUTER JOIN comments ON posts.id = comments.postId`;
  connection.query(sql, (err, res) => {
    if (err) {
      console.log(err);
      return;
    } else {
      result(res);
    }
  });
};

export const patch_post_method = (id, content, result) => {
  const sql = `UPDATE posts SET content = '${content}' WHERE id = '${id}'`;
  connection.query(sql, (err, res) => {
    if (err) {
      console.log(err);
      return;
    } else {
      result(res);
    }
  });
};

export const delete_post_method = (id, result) => {
  const sql = `DELETE FROM posts WHERE id = '${id}'`;
  connection.query(sql, (err, res) => {
    if (err) {
      console.log(err);
      return;
    } else {
      result(res);
    }
  });
};
