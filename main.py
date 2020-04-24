import requests
import time
from tqdm import tqdm

# вводные:
TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
user_id = 171691064
user_domain = 'eshmargunov'

# тело программы:
class User:
    '''
    Класс пользователя
    '''
    def __init__(self, token, user_in):
        self.token = token
        self.user_in = user_in
        self.user_id = self.user_info()['response'][0]['id']
        self.domain = self.user_info()['response'][0]['domain']

    def user_info(self):
        """
        принимает токен и входные данные от пользователя
        :return: id и domain пользователя для работы других методов
        """
        params = {
            'access_token': self.token,
            'user_ids': self.user_in,
            'fields': 'domain',
            'v': 5.52
        }
        responce = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        responce_dict = responce.json()
        time.sleep(0.4)
        return responce_dict

    def get_subscriptions(self):
        """
        на входе id и token
        :return: множество подписок пользователя
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
        print(f'Изучаем подписки {self.domain}...')
        responce_dict = responce.json()
        group_list = responce_dict['response']['groups']['items']
        group_set = set(group_list)
        time.sleep(0.4)
        return group_set

    def friends_get(self):
        '''
        на входе id и token
        :return: список id-друзей пользователя
        '''
        params = {
            'access_token': self.token,
            'user_id': self.user_id,
            'order': 'hints',
            'count': '200',
            'name_case': 'nom',
            'v': 5.52
        }
        responce = requests.get(
            'https://api.vk.com/method/friends.get',
            params
        )
        print(f'Изучаем друзей {self.domain}...')
        responce_dict = responce.json()
        friends_list = responce_dict['response']['items']
        time.sleep(0.4)
        return friends_list

    def friends_groups(self):
        """
        на входе id друзей и token
        :return: множество групп друзей
        """
        friends_groups_list = list()
        friends_list = self.friends_get()
        for user in tqdm(friends_list, desc='Изучаем группы друзей'):
            params = {
                'access_token': self.token,
                'user_id': user,
                'count': 200,
                'v': 5.52
            }
            responce = requests.get(
                'https://api.vk.com/method/users.getSubscriptions',
                params
            )
            responce_dict = responce.json()
            if 'response' in responce_dict.keys():
                group_list = responce_dict['response']['groups']['items']
                friends_groups_list.append(group_list)
                time.sleep(0.4)
            else:
                continue
        all_groups = list()
        for i in friends_groups_list:
            for j in i:
                all_groups.append(j)
        friends_groups_set = set(all_groups)
        return friends_groups_set

    def compare_groups(self):
        """
        принимаем множество групп друзей и групп пользователя
        :return: выводит конечный результат - список групп пользователя, в которых состоит только он
        """
        group_set = self.get_subscriptions()
        other_group_set = self.friends_groups()
        print('Собираем все вместе...')
        groups = group_set.difference(other_group_set)
        print('Готово!')
        print(f'Нашлось групп: {len(groups)}. \nВот они: {groups}')
        return groups


def main():
    user_into = input('Введите данные пользователя (id или domain): ')
    user = User(TOKEN, user_into)
    user.compare_groups()

main()