from django.contrib import admin
from . import models
from celery_tasks.main import celery_app
from django.template import loader
from django.conf import settings
import os

from goods.utils import get_categories
from goods.models import SKU


# Register your models here.


#重写save（）方法
class SKUAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(obj.id)

class SKUImageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(obj.sku.id)

        # 设置SKU默认图片
        sku = obj.sku
        if not sku.default_image_url:
            sku.default_image_url = obj.image.url
            sku.save()

    def delete_model(self, request, obj):
        sku_id = obj.sku.id
        obj.delete()
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(sku_id)

class GoodsCategoryAdmin(admin.ModelAdmin):
    #自定义类,监听删除和保存
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()
        from celery_tasks.html.tasks import generate_static_list_search_html
        generate_static_list_search_html.delay()

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        from celery_tasks.html.tasks import generate_static_list_search_html
        generate_static_list_search_html.delay()
        obj.delete()

admin.site.register(models.GoodsCategory,GoodsCategoryAdmin)
admin.site.register(models.GoodsChannel)
admin.site.register(models.Goods)
admin.site.register(models.Brand)
admin.site.register(models.GoodsSpecification)
admin.site.register(models.SpecificationOption)
admin.site.register(models.SKU,SKUAdmin)
admin.site.register(models.SKUSpecification)
admin.site.register(models.SKUImage,SKUImageAdmin)