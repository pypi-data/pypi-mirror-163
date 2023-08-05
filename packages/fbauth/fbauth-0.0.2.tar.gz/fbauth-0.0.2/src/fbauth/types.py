# -*- coding: utf-8 -*-
"""
    API - Strawberry Types
"""
import dataclasses as dc
import datetime
import typing

import fastberry as fb

from .database import model


# Create your <types> here.
class Date:
    datetime = lambda: datetime.datetime.now()
    date = lambda: datetime.date.today()
    time = lambda: datetime.datetime.now().time()


# Create your <types> here.
@model.sql(
    required=["name"],
    unique=["name"],
)
class Role:
    name: str
    perms: fb.JSON


@model.sql(
    required=["username", "email"],
    index=["username"],
    unique=["username", "email"],
)
class User:
    username: str
    password: str
    email: str
    is_disabled: bool = False
    is_staff: bool = False
    is_super_user: bool = False
    created_on: datetime.datetime = dc.field(default_factory=Date.datetime)
    # updated_on: datetime.datetime = dc.field(default_factory=Date.datetime)

    async def role(self) -> typing.Optional["Role"]:
        print(self)
        return None
