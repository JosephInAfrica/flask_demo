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
	username=db.Column(db.String(64),unique=True,index=True)
	role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
	password_hash=db.Column(db.String(128))
	confirmed=db.Column(db.Boolean,default=False)
	name=db.Column(db.String(64))
	location=db.Column(db.String(64))
	about_me=db.Column(db.Text())
	member_since=db.Column(db.DateTime(),default=datetime.utfnow)
	last_seen=db.Column(db.DateTime(),default=datetime.utcnow)
	avatar_hash=db.Column(db.String(32))
	posts=db.relationship('Post',backref='author',lazy='dynamic')
	followed=db.relationship('Follow',foreign_keys=[Follow.follower_id],backref=db.backref('follower',lazy='joined'),lazy='dynamic',cascade='all,delete-orphan')
	followers=db.relationship('Follow',foreign_keys=[Follow.followed_id],backref=db.backref('followed',lazy='joined'),lazy='dynamic',cascade='all,delete-orphan')
	comments=db.relationship('Comment',backref='author',lazy='dynamic')

	@staticmethod
	def generate_fake(count=100):
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py

		seed()
		for i in range(count):
			u=User(email=forgery_py.internet.email.address,username=forgery_py.internet.user_name(True),password=forgery_py.lorem_ipsum.word(),confirmed=True,name=forgery_py.address.city(),about_me=forgery_py.lorem_ipsum.sentence(),member_since=forgery_py.date.date(True))
			db.session.add(u)
			try:
				db.session.commit()
			except IntegrityEorr:
				db.session.rollback()

		@staticmethod
		def add_self_follows():
			for user in User.query.all():
				if not user.is_following(user):
					user.follow(user)
					db.session.add(user)
					db.session.commit()
					# where commit is applied. sometimes commit is not done after add or adaptation.

		def __init__(self,**kwargs):
			super(User,self).__init__(**kwargs)
			if self.role is None:
				if self.email==current_app.config['FLASKY_ADMIN']:
					self.role=Role.query.filter(Permission=0xff).first()

				if self.role is None:
					self.role=Role.query.filter_by(default=True).first()
			if self.email is nont None and self.avatar_hash is None:
				self.avatar_hash=hashlib.md5(self.email.encode('utf-8')).hexdigest()
			self.followed.append(Follow(followed=self))

		@property
		def password(self):
			raise AttributeError('password is not a readable attribute.')


		@password.setter
		def password(self,password):
			self.password_hash=generate_password_hash(password)

		def verify_password(self,password):
			


