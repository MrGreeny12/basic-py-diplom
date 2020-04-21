from main import User
from pprint import pprint

TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

user_id = 171691064
user_domain = 'eshmargunov'

eshmargunov = User(TOKEN, user_id)
responce = eshmargunov.get_subscriptions()
pprint(responce)

