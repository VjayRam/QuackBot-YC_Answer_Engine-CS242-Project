# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class CompaniesPipeline:
    def process_item(self, item, spider):
        return item




class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # Customize the file path (e.g., by company name)
        company_name = item.get('company_name', 'default').replace(' ', '_')
        image_name = os.path.basename(request.url)
        return f"{company_name}/{image_name}"

    def item_completed(self, results, item, info):
        # Filter successful downloads
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("No images downloaded")
        item['images'] = image_paths
        return item

