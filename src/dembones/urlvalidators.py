from urllib.parse import urlparse


def same_domain_up_path(current, target):
    """Verify target is upstream of current. Both fully qualified urls"""
    return current in target


def same_domain(current, target):
    """Verify target is in same domain as current. both fully qualified urls"""
    return urlparse(current)[1] == urlparse(target)[1]