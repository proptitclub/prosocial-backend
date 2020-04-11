import {
  get_group_method,
  patch_group_method,
  post_group_method,
  delete_group_method,
} from '../models';

import uuid from 'uuid';

class Group {
  constructor() {
    this.groups = [];
  }

  getAllGroups(req, res) {
    get_group_method(null, (err, groups) => {
      if (err) res.send(err);
      else {
        this.groups = groups;
        res.send(this.groups);
      }
    });
  }

  getGroupById(groupId, res) {
    get_group_method(groupId, (err, groups) => {
      if (err) res.send(err);
      else res.send(groups[0]);
    });
  }

  editGroup(group, res) {
    patch_group_method(group, (err, responseSV) => {
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

  addNewGroup(group, res) {
    post_group_method(
      {
        id: uuid(),
        group,
      },
      (err, responseSV) => {
        if (err) console.log(err);
        else res.send('Create Group Successfully');
      },
    );
  }

  deleteGroup(group, res) {
    delete_group_method(group, (err, responseSV) => {
      if (err) console.log(err);
      else res.send('Delete Group Succesfully');
    });
  }
}

export const groupController = new Group();
