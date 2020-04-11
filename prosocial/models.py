from django.db import models


class User(models.Model):
    username = ''
    password = ''
    displayName = ''
    dateOfBirth = ''
    className = ''
    phoneNumber = ''
    email = ''
    facebook = ''
    description = ''


class Post(models.Model):
    userId = ''
    groupId = ''
    content = ''
    time = ''
    type = ''


class Group(models.Model):
    name = ''
    description = ''


class Comment(models.Model):
    content = ''


class Reaction(models.Model):
    pass
