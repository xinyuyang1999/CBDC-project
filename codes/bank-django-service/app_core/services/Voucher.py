from app_core.models.Voucher import Voucher as VoucherModel
from app_core.services.ResolveRequest import ResolveRequest
from app_core.services.UUIDRandom import UUIDRandom
from app_core.models.User import User
from app_core.models.UserBalance import UserBalance
from django.http import HttpResponse
import json

class Voucher:
    def __init__(self):
        pass
    def generate_voucher(self,request):
        """
        用管理員帳戶生成代金券
        """
        role = ResolveRequest.ResolveRole(request)
        data = ResolveRequest.ResolvePost(request)
        # 若沒有使用者權限，則無法生成
        if role != 'administrator': 
            return HttpResponse(json.dumps({
                'code': 0,
                'message': 'User forbidden'
        }))
        token =UUIDRandom.random_uuid_string()[:10]
        voucher = VoucherModel()
        voucher.currency = data['amount']
        voucher.voucher_token = token
        voucher.save()

        return HttpResponse(json.dumps({
            'code': 1,
            'token': token
        }))

    def redeem_voucher(self,request):
        # 輸入資料擷取
        input_data = ResolveRequest.ResolvePost(request)
        input_voucher_token = input_data['voucher_token']
        
        # 取得點數卡資料庫實例
        voucher = VoucherModel.objects.filter(voucher_token=input_voucher_token)

        # 檢查Token是否有效
        if voucher.count() != 1:
            return HttpResponse(json.dumps({
                'code': 0,
                'message': 'Invalid voucher token'
            }))

        # 檢查點數卡是否被使用過
        if voucher[0].is_used == 1:
            return HttpResponse(json.dumps({
                'code': 0,
                'message': 'Voucher token is used'
            }))

        # 取得該點數卡的餘額
        currency_in_voucher = voucher[0].currency

        # 設置點數卡為已經使用過了
        voucher = voucher[0]
        voucher.is_used = 1
        voucher.save()

        # 更新貨幣總數
        user_id = ResolveRequest.ResolveUserID(request)
        user_balance = UserBalance.objects.filter(user_id=user_id)[0]
        user_balance.balance = user_balance.balance + currency_in_voucher
        user_balance.save()
        
        return HttpResponse(json.dumps({
            'code': 1,
            'message': 'The voucher successfully deposited into the bank'
        }))

