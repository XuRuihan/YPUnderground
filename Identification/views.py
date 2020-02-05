from django.http import JsonResponse
# from django.shortcuts import render
from django.middleware.csrf import get_token

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


def getToken(request):
    return JsonResponse({'ret': 'True', 'token': get_token(request)})


# let that=this;
# const url='http://127.0.0.1/api2/get_token';
# this.axios.get(url).then(res=>{
# // 先获取后台cookie
# let csrftoken=that.$cookie.get('csrftoken');
# const url='http://127.0.0.1/api2/post_test';
# // post 请求后台接口
# this.axios.post(url,{},{
#     headers:{
#     'X-CSRFtoken':csrftoken
#     }
# }).then(res=>{
#     console.log(res.data);
# }


@require_http_methods(['POST'])  # 必须使用post方法
@csrf_exempt  # csrf 豁免
def wxTest(request):
    print(request)
    if (request.method == 'GET'):
        print('wxTest using GET method')
        return JsonResponse({'ret': 'True', 'data': {'Sname': 'Jerry'}})
    elif (request.method == 'POST'):
        print('wxTest using POST method')
        return JsonResponse({'ret': 'True', 'data': {}})
    else:
        print('wxTest Failed')
        return JsonResponse({'ret': 'False', 'data': {}})
