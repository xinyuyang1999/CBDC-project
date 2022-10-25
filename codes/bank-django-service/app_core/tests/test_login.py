from django.test import TestCase
from ..models.Login import Login
from ..models.User import User
import redis
import requests
import json
import os


class LoginTestClass(TestCase):

    def setUp(self):
        # 網址路徑
        self.url = 'http://127.0.0.1:8000/api/login'
        # 使用者帳號與密碼的Hash
        self.account = "user"
        self.password = 'user'
        self.password_hash = "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb"
        # 建立測試用使用者資料
        User.objects.create(account = self.account)
        User.objects.create(password_hash = self.password_hash)
        # 建立 Redis 連線
        self.redis_connection_token_index = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
        self.redis_connection_user_index = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=1, password=os.environ['REDIS_PASSWORD'])
        
    def test_Login(self):
        login = Login()
        # 正確登入
        print("[登入測試] 正確登入測試")
        result = requests.get(self.url, params={'account': self.account, 'password':self.password})
        result_json_object = json.loads(result.text)
        self.assertEqual(result_json_object['code'], 1)
        token = self.redis_connection_user_index.get(self.account).decode('utf-8')
        
        print("[登入測試] 檢查Redis是否正確存有Token")
        asserted_token = result_json_object['token']
        self.assertEqual(token, asserted_token)
        
        print("[登入測試] 刪除Token")
        self.redis_connection_token_index.delete(token)
        self.redis_connection_user_index.delete(self.account)
        
        # 錯誤登入
        print("[登入測試] 錯誤登入測試")
        result = requests.get(self.url, params={'account': self.account, 'password':'wrong password'})
        result_json_object = json.loads(result.text)
        self.assertEqual(result_json_object['code'], 0)
        # self.assertTrue(False)
        # self.assertFalse(False)