from urllib.parse import urlparse


def same_domain(current, target):
    """Verify target is in same domain as current. both fully qualified urls"""
    return urlparse(current)[1] == urlparse(target)[1]


def same_domain_up_path(current, target):
    """Verify target is upstream of current. Both fully qualified urls"""
    return (
            same_domain(current, target)
            and urlparse(current)[2] in urlparse(target)[2]
            )
