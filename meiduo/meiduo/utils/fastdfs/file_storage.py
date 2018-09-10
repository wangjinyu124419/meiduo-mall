from django.conf import settings
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client



class Fastdfsstorage(Storage):
    def __init__(self,client_conf=None,base_url=None):
        # if client_conf==None:
        #     self.client_conf=settings.FDFS_CLIENT_CONF
        self.client_conf=client_conf or settings.FDFS_CLIENT_CONF
        self.base_url=base_url or settings.FDFS_BASE_URL


    def _open(self,name,mode='rb'):
        #因为源码要求必须实现,但储存文件不需要打开,所以return none,pass掉
        pass
    def _save(self,name,content):
        # client = Fdfs_client('meiduo_mall/utils/fastdfs/client.conf')
        # client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        client = Fdfs_client(self.client_conf)
        # ret = client.upload_by_filename('/Users/zhangjie/Desktop/01.jpeg')

        ret=client.upload_by_buffer(content.read())

        #判断文件是否上传成功

        """
        {'Group name': 'group1',
        'Remote file_id': 'group1/M00/00/00/wKhnhluSuYeAIc39AAC4j90Tziw56.jpeg',
        'Status': 'Upload successed.',
        'Local file name': '/Users/zhangjie/Desktop/01.jpeg',
        'Uploaded size': '46.00KB',
        'Storage IP': '192.168.103.132'}
        """
        if ret.get('Status')!='Upload successed.':
            raise Exception('upload file failed ')
        file_id=ret.get('Remote file_id')
        #自定义文件存储系统之后,我们只需要返回file_di即可,
        #将来温江存储系统会自动讲file_id存储到对应的ImageFile字段中
        return file_id

    def exists(self, name):
        #判断文件是否存在,判断本地是否存储了文件
        return False
    def url(self,name):
        #返回文件绝对 路径
        # myurl='http://192.1 68.188.143:8888/'+name
        return self.base_url+name
