from rest_framework.views import APIView
from rest_framework.response import Response
import redis

class BigListView(APIView):
    def get(self, request):
        # redis-py sẽ tự dùng hiredis nếu đã cài
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        # Giả lập dữ liệu lớn
        if not r.exists('big_list'):
            r.lpush('big_list', *map(str, range(10000)))
        
        data = r.lrange('big_list', 0, -1)
        return Response({'count': len(data), 'sample': data[:5]})