import listparser as lp
from urllib.parse import urlparse
import validators
import tabulate

def parse(file_name):
  result = lp.parse(file_name)
  rst = {}
  for feed in result.feeds:
      for tag in feed['tags']:
          url = feed['url']
          uri = urlparse(url)
          origin = '{uri.scheme}://{uri.netloc}/'.format(uri=uri)

          feed_title = feed['title'].replace('|', '\|')
          title = feed_title if 'rsshub.app' in origin else '[{}]({})'.format(feed_title, origin)

          if validators.url(url):
            status = '![](https://img.shields.io/website?label=status&style=flat-square&url={})'.format(url)
            i = [title, url, status]
            rst.setdefault(tag, []).append(i)
  return rst

def write_to_md(feeds_list, filename):
  with open(filename, 'wt', encoding="utf-8") as f:
    head_str = (
      "# Feeds\n"
      "> High quality RSS feeds for web developers.\n\n"
      "You can also download [index.opml](./index.opml) directly.\n"
      "![image](https://user-images.githubusercontent.com/13595509/118289469-f7b27b80-b507-11eb-968d-95bdc056eb5d.png)\n"
    )
    f.write(head_str)
    for tag, feed_list in feeds_list.items():
        f.write("# " + tag + "\n")
        f.write(tabulate.tabulate(feed_list, headers=["Title", "Feed", "Status"], tablefmt="pipe"))
        f.write("\n")

    tail_str = (
      "# Development\n"
      "Convert the opml file into markdown\n\n"
      "```bash\n"
      "$ pip install -r requirements.txt\n"
      "$ python __init__.py\n"
      "```\n"
    )
    f.write(tail_str)

feeds_list = parse('./index.opml')
md_str = write_to_md(feeds_list, './README.md')


