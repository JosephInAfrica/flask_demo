from datetime import datetime 
import hashlib
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serialiazer
from markdown import markdown 
import bleach
from flask import current_app ,request,url_for
from flask_login import UserMixin, AnonymousUser
from app.exceptions import ValidationError
from . import db ,login_manager

class Permission:
	FOLLOW=0x01
	COMMNET=0x02
	WRITE_ARTICLES=0x04
	MODERATE_COMMENTS=0x08
	ADMINISTER=0x80

class Role(db.Model):
	__tablename__='roles'
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(64),unique=True)
	default=db.Column(db.Boolean,default=False,index=True)
	permissions=db.Column(db.Integer)
	users=db.relationship('User',backref='role',lazy='dynamic')

	@staticmethod
	def insert_roles():
		roles={
		'User':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES,True),
		'Moderator':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLESS|Permission.MODERATE_COMMENTS,False),
		'Administrator':(0xff,False)

		}
		for r in roles:
			role=Role.query.filter_by(name=r).first()
			if role is None:
				role=Role(name=r)
			role.permissions=roles[r][0]
			role.default=roles[r][1]
			db.session.add(role)
		db.session.commit()
	def __repr__(self):
		return '<Role %r>'% self.name

class Follow(db.Model):
	__tablename__='follows'
	follower_id=db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
	followed_id=db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
	timestamp=db.Column(db)

class User(UserMixin, db.Model):
	__tablename__='users'
	id=db.Column(db.String(64),unique=True, index=True)
	username=db.Column()


