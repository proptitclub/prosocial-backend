import { connection } from '../database';

import { tbl_UGR } from '../helpers';

export const get_user_group_method = (req, result) => {
  let query = `SELECT * FROM ${tbl_UGR}`;
  connection.query(query, (error, res) => {
    if (error) {
      result(error, null);
    }
    result(null, res);
  });
};

export const post_user_group_method = ({ userId, roleId, groupId }, result) => {
  connection.query(
    `INSERT INTO ${tbl_UGR} (userId, roleId, groupId) VALUES ('${userId}', '${roleId}', '${groupId}')`,
    (error, res) => {
      if (error) {
        result(error, null);
      }
      result(null, res);
    },
  );
};

export const patch_user_group_method = (
  { userId, groupId, roleId },
  result,
) => {
  connection.query(
    `UPDATE ${tbl_UGR} SET roleId = "${roleId}" WHERE userId = "${userId}" AND groupId = "${groupId}"`,
    (err, res) => {
      if (err) result(err, null);
      result(null, res);
    },
  );
};

export const delete_user_group_method = (
  { userId, roleId, groupId },
  result,
) => {
  connection.query(
    `DELETE FROM ${tbl_UGR} WHERE userId = "${userId}" AND roleId = "${roleId}" AND groupId = "${groupId}`,
    (err, res) => {
      if (err) {
        result(err, null);
      }
      result(null, res);
    },
  );
};
