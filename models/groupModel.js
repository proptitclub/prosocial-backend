import { connection } from '../database';

export const get_group_method = (filterID, result) => {
  let query = 'SELECT * FROM `groups`';
  if (filterID) query += ` WHERE id = "${filterID}"`;
  connection.query(query, (error, res) => {
    if (error) {
      console.log(error);
      return;
    }
    result(null, res);
  });
};

export const post_group_method = ({ id, group }, result) => {
  connection.query(
    `INSERT INTO groups(id, name) VALUES ('${id}','${group.name}')`,
    (error, res) => {
      if (error) {
        console.log(error);
        return;
      }
      result(null, res);
    },
  );
};

export const patch_group_method = (group, result) => {
  connection.query(
    `UPDATE groups SET name = "${group.name}" WHERE id = "${group.id}"`,
    (err, res) => {
      if (err) result(err, null);
      result(null, res);
    },
  );
};

export const delete_group_method = (group, result) => {
  connection.query(
    `DELETE FROM groups WHERE id = "${group.id}"`,
    (err, res) => {
      if (err) result(err, null);
      result(null, res);
    },
  );
};
