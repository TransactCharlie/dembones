# dembones
Generate Skeleton Map of website showing assets and links

## Quickstart
Docker builds are created on pushes and hosted on dockerhub. Quickest way to use dembones is:

```
# docker run transactcharlie/dembones --help
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  scrape
  test
```

Issuing --help on either of the commands shows you the possible options

```
# docker run transactcharlie/dembones scrape --help
Usage: cli.py scrape [OPTIONS] URL

Options:
  -c, --max-concurrency INTEGER   Max fetch tasks at any one time
  -d, --max-depth INTEGER         Maximum recursion when collecting URLS
  -t, --target-validator [same-domain|same-domain-up-path]
                                  How to decide if we should recurse a link
  -v, --verbose                   Verbosity (-v, -vv, -vvv)
  --help                          Show this message and exit.
```

Each parameter for **scrape** action has a default value so you can simply give scrape a URL and you'll get a json payload back to stdout
```
# docker run transactcharlie/dembones scrape "http://www.foo.com/"
{
    "http://www.foo.com/": {
        "title": "Foo.com",
        "links": [
            "http://www.foo.com/",
            "http://www.foo.com/digimedia_privacy_policy.html"
        ],
        "images": [
            "http://www.foo.com/media/W1siZiIsIjIwMTIvMDQvMjYvMjAvMTEvNDkvNDI2L2NvcmRvdmFiZWFjaC5qcGciXSxbInAiLCJ0aHVtYiIsIjc1MHgyMDAjIl1d/cordovabeach.jpg"
        ],
        "scripts": [
            "http://www.foo.com/assets/application-ed93414a748943685ca41c9e0c475bc5.js",
            "http://www.foo.com/assets/abp2-4831d5b24977f8140fd9aa25543527f2.js",
            "http://www.foo.com/assets/ads-832e97bfd2d3e735f6dc8a30dd7190bc.js",
            "http://www.google.com/adsense/domains/caf.js"
        ]
    },
    "http://www.foo.com/digimedia_privacy_policy.html": {
        "title": "",
        "links": [
            "http://www.networkadvertising.org/managing/opt_out.asp",
            "mailto:admin@digimedia.com"
        ],
        "images": [],
        "scripts": []
    }
}
```

## Developing
Dembones requires python supporting the new await syntax (3.5 +). Recommended interpreter version is pytohn 3.6.
The easiest way to develop locally is to create a virtulenv with the requirements.txt.

Fork Dembones in github and clone your repo
```
git clone git@github.com:TransactCharlie/dembones.git 
cd dembones
virtualenv env --no-site-packages --python=python3.6
PYTHONPATH=src pytest tests -v
```


