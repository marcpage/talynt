#!/usr/bin/env python3

""" Data model
"""


import hashlib
import enum

from talynt.table import Table, Identifier, String, ForeignKey
from talynt.table import Enum, Fixed, Money, Integer, Date
import talynt.database


class User(Table):
    """User info"""

    _db = None
    id = Identifier()
    name = String(50, allow_null=False)
    email = String(50, allow_null=False)
    password_hash = String(64, allow_null=False)

    @staticmethod
    def hash_password(text):
        """hash utf-8 text"""
        hasher = hashlib.new("sha256")
        hasher.update(text.encode("utf-8"))
        return hasher.hexdigest()

    @staticmethod
    def create(email: str, password: str, name: str, pw_hashed=False):
        """create a new user entry"""
        assert password is not None
        user = User(
            email=email,
            password_hash=password if pw_hashed else User.hash_password(password),
            name=name,
            _normalize_=False,
        ).denormalize()
        created = User._db.insert(Table.name(User), **user)
        return User(**created)

    @staticmethod
    def fetch(user_id: int):
        """Get a user by its id"""
        found = User._db.get_one_or_none(
            Table.name(User),
            _where_="id = :user_id",
            user_id=user_id,
        )
        return None if found is None else User(**found)

    @staticmethod
    def lookup(email: str):
        """Get a user by email (case insensitive)"""
        found = User._db.get_one_or_none(
            Table.name(User), _where_="email LIKE :email", email=email
        )
        return None if found is None else User(**found)

    @staticmethod
    def every():
        """Get list of all users"""
        return [User(**u) for u in User._db.get_all(Table.name(User))]

    @staticmethod
    def total():
        """Count total users"""
        return User._db.get_one_or_none(Table.name(User), "COUNT(*)")["COUNT(*)"]

    def password_matches(self, password):
        """Verify that the user's password matches the given password"""
        return User.hash_password(password) == self.password_hash

    def change(self, **_to_update_):
        """Change information about the user"""
        assert "id" not in _to_update_
        assert "password" not in _to_update_ or _to_update_["password"] is not None
        password = _to_update_.get("password", None)

        if password is not None:
            _to_update_["password_hash"] = User.hash_password(password)
            del _to_update_["password"]

        for field in _to_update_:
            _to_update_[field] = Table.denormalize_field(
                User, field, _to_update_[field]
            )

        User._db.change(
            Table.name(User),
            "user_id",
            _where_="id = :user_id",
            user_id=self.id,
            **_to_update_,
        )

        for field, value in _to_update_.items():
            self.__dict__[field] = Table.normalize_field(User, field, value)


class Skill(Table):
    """Skills or experience"""

    _db = None
    id = Identifier()
    name = String(50, allow_null=False)

    @staticmethod
    def create(name: str):
        """Create a new skill"""
        link = Skill(name=name)


class Employment(enum.Enum):
    """Type of employment"""

    FULL = 1  # Full time
    PART = 2  # Part time
    CTRC = 3  # Contract


class Job(Table):
    """job description"""

    _db = None
    id = Identifier()
    url = String(2083)
    title = String(50)
    company = String(50)
    salary_low = Money()
    salary_high = Money()
    employment = Enum(Employment)
    location = String(50)
    text = String(4096)


class UserJob(Table):
    """bookmarked jobs"""

    _db = None
    id = Identifier()
    user_id = ForeignKey("User", allow_null=False)
    job_id = ForeignKey("Job", allow_null=False)


class Level(enum.Enum):
    """Levels of experience"""

    NONE = 0  # No experience
    NOOB = 1  # Tinkering
    HOBY = 2  # Hobby level
    BGNR = 3  # Some professional
    PEER = 4  # Professional
    MSTR = 5  # Expert


class JobSkill(Table):
    """Skill required for a job"""

    _db = None
    id = Identifier()
    job_id = ForeignKey("Job", allow_null=False)
    skill_id = ForeignKey("Skill", allow_null=False)
    years = Integer()
    level = Enum(Level)
    priority = Integer()


class UserSkill(Table):
    """Skill levels"""

    _db = None
    id = Identifier()
    user_id = ForeignKey("User", allow_null=False)
    skill_id = ForeignKey("Skill", allow_null=False)
    years = Integer()
    years_since = Integer()
    level = Enum(Level)
    priority = Integer()
    example = String(4096)


# pylint: disable=too-few-public-methods
class Database:
    """stored information"""

    tables = [User, Skill, Job, JobSkill, UserSkill, UserJob]

    def __init__(self, db_url):
        """create db
        db_url - a URL for the database
        """
        self.__db = talynt.database.Connection.connect(
            db_url, default_return_objects=False
        )
        description = Table.database_description(*Database.tables)
        self.__db.create_tables(**description)

        for table in Database.tables:
            table._db = self.__db

    def close(self):
        """close down the connection to the database"""
        self.__db.close()
