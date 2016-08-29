import random
import sys
import json

import spam
import model

class ContentManager:
	def __init__(self, operation, repository, configuration):
		self.operation = operation
		self.repository = repository
		self.configuration = configuration
		self.spam_validator = spam.SpamDetector(self.operation, self.repository, self.configuration)

		self.tags = list(map(lambda tag: tag.strip().encode('cp1251').decode('utf-8'), self.configuration.instalike_tags.split(',')))
		
		self.photos = []
		self.photos_from_model = []
		self.users_from_model = []
		self.activities = []

	def get_photos(self):
		self.photos_from_model = []
		self.users_from_model = []

		no_of_photos = random.randint(2,10)

		for tag in self.tags:
			try:
				self.log('getting photos from tag {0}...'.format(tag))
				self.photos = self.operation.get_photos_by_tag(tag)
			except TypeError:
				self.log('oops! someting went wrong while fetching photos')

		# get details for each photo
		if not self.photos:
			return []
		for photo in self.photos:
			photo_details = self.operation.get_photo_details(photo['code'])
			if (photo_details):
				photo_instance = model.Photo().from_json(photo_details)
				self.repository.merge_photo(photo_instance)
				self.photos_from_model.append(photo_instance)

				user_details = self.operation.get_user_details(photo_instance.owner_username.replace('\'',''))
				if (user_details):
					user_instance = model.User().from_json(user_details)
					self.repository.merge_user(user_instance)
					self.users_from_model.append(user_instance)

		self.filter_photos()

		if (len(self.photos_from_model) < no_of_photos):
			no_of_photos = len(self.photos_from_model)

		self.photos_from_model = random.sample(self.photos_from_model, no_of_photos)
		self.users_from_model = self.spam_validator.validate_users(self.users_from_model)

		return self.photos_from_model

	def get_users(self):
		return self.users_from_model

	def get_users_to_unfollow(self):
		response = self.repository.get_users_to_unfollow()
		if(response):
			return json.loads(response)
		return []

	def get_activity(self):
		self.activities = []
		activities_json = self.operation.get_activity()

		if (activities_json):
			for json_node in activities_json:
				activity_model = model.Activity().from_json(json_node)
				self.activities.append(activity_model)
		return self.activities

	def filter_photos(self):
		self.photos_from_model = self.spam_validator.validate_photos(self.photos_from_model)
		self.log('downloaded {0} valid photos'.format(len(self.photos_from_model)))
		

	def log(self, text):
		try:
			print(text)
		except Exception:
			print('Error with text encoding. Try typing: export PYTHONIOENCODING=utf-8')