import base64

import pickle
from django_redis import get_redis_connection

def merge_cart_cookie_to_redis(request,response,user):
    #读取cookie数据
    #操作cookie
    cart_str = request.COOKIES.get('cart')
    if not cart_str:
        return response

    cart_str_bytes = cart_str.encode()
    # 将bytes的类型的字符串转成bytes类型的字典
    cart_dict_bytes = base64.b64decode(cart_str_bytes)

    # 讲bytes类型的字典转成标准字典
    cookie_cart_dict = pickle.loads(cart_dict_bytes)

    # user=request.user
    redis_conn=get_redis_connection('cart')

    redis_cart_dict=redis_conn.hgetall('cart_%s'%user.id)
    redis_cart_select=redis_conn.smembers('selected_%s'%user.id)
    print(type(redis_cart_select))
    sku_ids=cookie_cart_dict.keys()

    for sku_id in sku_ids:
        count=cookie_cart_dict[sku_id]['count']
        redis_cart_dict[sku_id]=count

        if cookie_cart_dict[sku_id]['selected']:
            redis_cart_select.add(sku_id)

    redis_cart_dict1111=redis_conn.hgetall('cart_%s'%user.id)
    redis_conn.hmset('cart_%s'%user.id,redis_cart_dict)
    redis_conn.sadd('selected_%s'%user.id,*redis_cart_select)

    response.delete_cookie('cart')
    return response