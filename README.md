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
PYTHONPATH=src python cli test
```

The src folder requires to be in the PYTHONPATH env var. This is so that you can run the unit tests against an installed version of dembones in the future independently of the source code.

## Build Status
[![Build Status](https://travis-ci.org/TransactCharlie/dembones.svg?branch=master)](https://travis-ci.org/TransactCharlie/dembones)
[![](https://images.microbadger.com/badges/image/transactcharlie/dembones.svg)](https://microbadger.com/images/transactcharlie/dembones "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/version/transactcharlie/dembones.svg)](https://microbadger.com/images/transactcharlie/dembones "Get your own version badge on microbadger.com")

* Travis-ci.org builds a docker image on any push and tags master branch pulls with the :latest tag. [View Travis Build History](https://travis-ci.org/TransactCharlie/dembones/builds)
* The DockerHub repository is [transactcharlie/dembones](https://hub.docker.com/r/transactcharlie/dembones/)
* Image details can be [found on Microbadger](https://microbadger.com/images/transactcharlie/dembones)

## TODO
* Visualisation of the collected websites as a directed graph using networkx and plotly. (See the scratch/graph_plotting folder for a POC)
* Exponential Backoff / Jitter during collection
* Avoid Bot Detection / Robots.txt