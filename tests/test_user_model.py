class UserModelTestCase(unittest.TestCase):

	def test_user_role(self):
		u=User(email='john@example.com',password='cat')
		self.assertTrue(u.can(Permission.FOLLOW))
		self.assertTrue(u.can(Permission.COMMENT))
		self.assertTrue(u.can(Permission.WRITE))
		self.assertFalse(u.can(Permission.MODERATE))
		self.assertFalse(u.can(Permission.ADMIN))

	def test_anonymous_user(self):
		u=AnonymousUser()
		self.assertFalse(u.can(Permission.FOLLOW))
		self.assertFalse(u.can(Permission.COMMENT))
		self.assertFalse(u.can(Permission.WRITE))
		self.assertFalse(u.can(Permission.MODERATE))
		self.assertFalse(u.can(Permission.ADMIN))

		