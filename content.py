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

		self.mediaList = []
		self.unfilteredMediaList = []

		self.userList = [] # List of media used to find users.
		self.unfollowUserList = [] # List of user ID.


	def get_media_count(self):
		return len(self.mediaList)

	def get_next_media(self):
		if(len(self.mediaList) == 0):
			if(not self.scrap_media()):
				return None

		return self.mediaList.pop(0)

	def get_user_count(self):
		return len(self.userList)

	def get_next_user(self):
		if(len(self.unfilteredMediaList) == 0):
			if (not self.scrap_media()):
				return None

		if(len(self.userList) == 0):
			if(not self.scrap_users()):
				self.log('Error getting users.')
				return None

		return self.userList.pop(0)

	def scrap_users(self):
		self.log('Scrapping & Validating users...')
		user_amount = random.randint(3, 10)

		for media in self.unfilteredMediaList:
			user = self.operation.get_user_details(media.owner_username.replace('\'',''))
			if (user):
				user_instance = model.User().from_json(user)
				self.repository.persist_user(user_instance)
				self.userList.append(user_instance)

		# Validate user.
		self.userList = self.spam_validator.validate_users(self.userList)
		if (user_amount > len(self.userList)):
			user_amount = len(self.userList)

		self.userList = random.sample(self.userList, user_amount)

		if(len(self.userList) == 0):
			self.log('could not get valid users.')
			return False

		return True

	def scrap_media(self):
		self.log('scrapping & validating media...')

		response = False
		if(self.configuration.instalike_like_feed):
			response = self.scrap_feed_media() or response
		response = self.scrap_tag_media() or response

		return response

	def scrap_tag_media(self):
		self.log('tag media...')

		bytag = self.tags.pop(0)
		self.tags.append(bytag)

		tag_media = self.operation.get_photos_by_tag(bytag)

		return self.process_media(tag_media)

	def scrap_feed_media(self):
		self.log('feed media...')

		feed_media = self.operation.get_feed_media()

		return self.process_media(feed_media, 0)

	def process_media(self, media_array, feed = 1):
		media_amount = random.randint(3, 10)
		if(media_array):
			for media in media_array:
				if feed == 0:
					media_details = self.operation.get_photo_details(media['node']['shortcode'])
				else:
					media_details = self.operation.get_photo_details(media['node']['shortcode'])

				if(media_details):
					media_instance = model.Photo().from_json(media_details)
					self.unfilteredMediaList.append(media_instance)
		else:
			return False

		# Validate and pick random photos.
		media_list = self.spam_validator.validate_photos(self.unfilteredMediaList)

		if (media_amount > len(media_list)):
			media_amount = len(media_list)

		self.mediaList.extend(random.sample(media_list, media_amount))

		if(len(self.mediaList) == 0):
			return False

		return True


	def get_photos(self):
		self.photos_from_model = []
		self.users_from_model = []

		no_of_photos = random.randint(2,10)

		for tag in self.tags:
			try:
				self.log('getting photos from tag {0}...'.format(tag))
				self.photos = self.operation.get_photos_by_tag(tag)
			except TypeError:
				self.log('oops! someting went wrong while fetching photos.')

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

	def get_next_user_to_unfollow(self):
		if(len(self.unfollowUserList) == 0):			
			if(not self.load_users_to_unfollow()):
				return None

		return self.unfollowUserList.pop(0)

	def load_users_to_unfollow(self):
		response = self.repository.get_users_to_unfollow()
		if(response):
			self.unfollowUserList = json.loads(response)
			return True

		return False

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
		self.log('downloaded {0} valid media.'.format(len(self.photos_from_model)))
		

	def log(self, text):
		try:
			print(text)
		except Exception:
			print('error with text encoding. Try typing: export PYTHONIOENCODING=utf-8')