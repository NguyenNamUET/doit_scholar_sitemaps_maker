import datetime
import os
import re
from jinja2 import Template

from helpers.utilities import store_gz, load_jsonl_from_gz, make_sitemap_paper_title

PATH = "/home/nguyennam/Downloads/data/20201005_234221"
STORAGE_PATH = "/home/nguyennam/Desktop"


def make_base_sitemap():
    base_sitemaps = {"pages":[], "changefreq":"monthly"}
    for sitemap in os.listdir(PATH):
        loc = sitemap.replace("_","-paper-")
        base_sitemaps["pages"].append(f"http://51.210.251.250:3400/{loc}.xml.gz")

    sitemap_template = '''<?xml version="1.0" encoding="UTF-8"?>
    <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {% for page in pages %}
        <sitemap>
            <loc>{{page}}</loc>
            <changefreq>{{changefreq}}</changefreq>    
        </sitemap>
        {% endfor %}
    </sitemapindex>'''

    template = Template(sitemap_template)
    sitemap_output = template.render(base_sitemaps)
    # Write the File to Your Working Folder
    store_gz(sitemap_output, f"{STORAGE_PATH}/base_sitemap/sitemap_paper_index.xml.gz")


def make_sitemap_xml(sitemap_path):
    base_sitemaps = {"pages": [], "changefreq": "weekly", "priority":0.8}
    for sitemap in os.listdir(os.path.join(PATH, sitemap_path)):
        if re.search(".json.gz", sitemap) is not None:
            paper = load_jsonl_from_gz(os.path.join(PATH, sitemap_path, sitemap))
            title = make_sitemap_paper_title(paper["title"])
            id = paper["paperId"]
            lastmod_date = datetime.datetime.now().strftime('%Y-%m-%d')
            base_sitemaps["pages"].append((f"http://51.210.251.250:3400/{title}.p-{id}", lastmod_date))
    print(base_sitemaps)
    sitemap_template = '''<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            {% for page in pages %}
            <url>
                <loc>{{page[0]}}</loc>
                <lastmod>{{page[1]}}</lastmod>
                <priority>{{priority}}</priority>
                <changefreq>{{changefreq}}</changefreq>    
            </url>
            {% endfor %}
        </urlset>'''

    template = Template(sitemap_template)
    sitemap_output = template.render(base_sitemaps)
    # Write the File to Your Working Folder
    id = re.findall("\d+", sitemap_path)[0]
    store_gz(sitemap_output, f"{STORAGE_PATH}/paper_sitemaps/sitemap-paper-{id}.xml.gz")


if __name__ == '__main__':
    make_base_sitemap()
    for sitemap in os.listdir(PATH):
        make_sitemap_xml(sitemap)
