import scrapy
import json

class AmazonSpider(scrapy.Spider):
    name = 'amazon_spider'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/dp/B00005BVRQ']

    def parse(self, response):
        data = {}

        data["Product name"] = response.css('#productTitle::text').get().strip()
        data["Current product price"] = response.css('.a-offscreen::text').get().strip()
        data["Trademark of the product"] = response.css('#bylineInfo::text').get().strip()
        data["Number of reviews"] = response.css('#acrCustomerReviewText::text').get().strip()
        data["Rating"] = response.css('.a-icon-alt::text').get().strip()

        buy_box_seller = response.css('#merchant-info span.a-declarative span.a-size-small::text').getall()
        if buy_box_seller:
            buy_box_seller = [s.strip() for s in buy_box_seller]
            data["Buy-Box Sellers"] = {
                "Ships From": buy_box_seller[0] if len(buy_box_seller) > 0 else "",
                "Sold By": buy_box_seller[1] if len(buy_box_seller) > 1 else ""
            }

        other_sellers = response.css('.a-section.a-spacing-small.a-spacing-top-small span.a-size-small.a-color-secondary::text').getall()
        data["Other Sellers"] = [s.strip() for s in other_sellers]

        total_sellers = len(other_sellers) + 1 
        data["Total Sellers"] = total_sellers

        variations = response.css('.a-size-base.a-text-bold span::text').getall()
        data["Variations"] = [v.strip() for v in variations]

        iframe_src = response.xpath('//iframe/@src').get()
        if iframe_src:
            data["Iframe Src"] = iframe_src.strip()

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)