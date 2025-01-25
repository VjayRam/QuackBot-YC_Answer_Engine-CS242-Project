import json
import scrapy


def make_start_urls_list():
    """Returns a list with the start URLs."""
    with open('scrapy-project/ycombinator/start_urls.txt', 'r') as f:
        return eval(f.read())


class YCombinator(scrapy.Spider):
    """Crawls ycombinator.com/companies and extracts data about each company."""
    name = 'YCombinatorScraper'
    start_urls = make_start_urls_list()

    def parse(self, response):
        # Extract JSON data
        st = response.css('[data-page]::attr(data-page)').get()
        if st is not None:
            # Load the JSON object and set the variable for the 'Company' data
            jo = json.loads(st)['props']
            jc = jo['company']
            
            # Extract image URLs (e.g., company logo, banner, etc.)
            image_urls = response.css('img::attr(src)').getall()  # Adjust selectors as needed
            
            yield {
                'company_id': jc['id'],
                'company_name': jc['name'],
                'short_description': jc['one_liner'],
                'long_description': jc['long_description'],
                'batch': jc['batch_name'],
                'status': jc['ycdc_status'],
                'tags': jc['tags'],
                'location': jc['location'],
                'country': jc['country'],
                'year_founded': jc['year_founded'],
                'num_founders': len(jc['founders']),
                'founders_names': [f['full_name'] for f in jc['founders']],
                'team_size': jc['team_size'],
                'website': jc['website'],
                'cb_url': jc['cb_url'],
                'linkedin_url': jc['linkedin_url'],
                'image_urls': image_urls,  # Add extracted image URLs
            }
