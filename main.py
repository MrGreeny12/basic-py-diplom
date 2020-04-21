from pprint import pprint
import requests

TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

user_id = 171691064
user_domain = 'eshmargunov'

# methods = список друзей -> список групп друзей -> те группы, которых нет в словарь -> в файл json
# два класса -> все методы пользователя в одном -> отдельный класс с методами выискивания групп -> общая функция
# класс испытуемого - как константа. Мы сначала получаем данные о пользователе, а потом в рамках другого класса
# проводим сравнение id всех групп между пользователями. После этого, мы каждую группу приводим в нужный вид
# и переносим во вновь созданый json файл

class User:
    '''
    Класс пользователя
    '''
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def __and__(self, other_user):
        '''
        other_user - это другой экземпляр класса user
        производит сравнение списков id двух экземпляров класса
        :param other_user: экземпляр класса, с которым нужно сравнить
        :return: список id общих друзей
        вывести список друзей, а потом через перебор циклом сравнивать всех друзей с искомым персонажем
        '''
        self.user_gr_list = self.get_subscriptions()['response']['groups']
        self.other_user_gr_list = other_user.get_subscriptions()['response']['groups']
        self.common_list = []
        for i in self.other_user_gr_list:
            for j in self.user_gr_list:
                if j != i:
                    self.common_list.append(j)
                    break
        return self.common_list

    def get_subscriptions(self):
        """

        :return:
        """
        params = {
            'access_token': self.token,
            'user_id': self.user_id,
            'count': 200,
            'v': 5.52
        }
        responce = requests.get(
            'https://api.vk.com/method/users.getSubscriptions',
            params
        )
        return responce.json()

    def friends_get(self):
        '''
        принимают параметры запроса
        :return: словарь с данными по методу friends.get vk
        '''
        params = {
            'access_token': self.token,
            'user_id': self.user_id,
            'order': 'hints',
            'count': '200',
            # 'fields': 'first_name, last_name',
            'name_case': 'nom',
            'v': 5.52
        }
        responce = requests.get(
            'https://api.vk.com/method/friends.get',
            params
        )
        responce_dict = responce.json()
        users = []
        friends_list = responce_dict['response']['items']
        for id_user in friends_list:
            user = User(self.token, id_user)
            users.append(user)
        return users

    def domain_get(self):
        '''
        '''
        params = {
            'access_token': self.token,
            'user_id': self.user_id,
            'fields': 'domain',
            'v': 5.52
        }
        domain_responce = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        return domain_responce.json()

eshmargunov = User(TOKEN, user_id)
responce = eshmargunov.get_subscriptions()
pprint(responce)

class User_group():
    pass