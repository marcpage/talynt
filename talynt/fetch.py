""" Handle fetching raw job descriptions """


import urllib.request


def job_description(url):
    """Fetches the given URL contents"""

    request = urllib.request.Request(
        url,
        data=None,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) "
                + "AppleWebKit/537.36 (KHTML, like Gecko) "
                + "Chrome/35.0.1916.47 Safari/537.36"
            )
        },
    )

    with urllib.request.urlopen(request) as stream:
        return stream.read().decode("utf-8")
