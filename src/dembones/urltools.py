from urllib.parse import urlparse, urldefrag


def validate_same_domain(current, target):
    """Verify target is in same domain as current. both fully qualified urls"""
    return urlparse(current)[1] == urlparse(target)[1]


def validate_same_domain_up_path(current, target):
    """Verify target is upstream of current. Both fully qualified urls"""
    return (
        validate_same_domain(current, target)
        and urlparse(current)[2] in urlparse(target)[2]
            )


def strip_fragment_identifier(url):
    """Strips any fragment id from a url"""
    return urldefrag(url)[0]
