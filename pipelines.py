from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class CustomImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("Image Pipeline is working")
        return Request(item['image_url'], meta={'image_name': item['image_name']})

    def file_path(self, request, response=None, info=None, *, item=None):
        print(request.meta)
        return f"{request.meta['image_name']}.png"