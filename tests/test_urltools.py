import dembones.urltools as ut


def test_same_domain_validator_same_domain_same_protocol():
    validator = ut.validate_same_domain
    current = "http://www.foo.com"
    target = "http://www.foo.com/bar"
    assert validator(current, target)


def test_same_domain_validator_same_domain_different_protocol():
    validator = ut.validate_same_domain
    current = "http://www.foo.com"
    target = "https://www.foo.com/bar"
    assert validator(current, target)


def test_same_domain_validator_different_hostname():
    validator = ut.validate_same_domain
    current = "http://www.foo.com"
    target = "https://www.zoo.com/bar"
    assert validator(current, target) is False


def test_same_domain_up_path_validator_same_domain_same_protocol():
    validator = ut.validate_same_domain_up_path
    current = "http://www.foo.com"
    target = "http://www.foo.com/bar"
    assert validator(current, target)


def test_same_domain_up_path_validator_same_domain_different_protocol():
    validator = ut.validate_same_domain_up_path
    current = "http://www.foo.com"
    target = "https://www.foo.com/bar"
    assert validator(current, target)


def test_same_domain_up_path_validator_different_hostname():
    validator = ut.validate_same_domain_up_path
    current = "http://www.foo.com"
    target = "https://www.zoo.com/bar"
    assert validator(current, target) is False


def test_same_domain_up_path_validator_forbids_backwards_path():
    validator = ut.validate_same_domain_up_path
    current = "http://www.foo.com/bar"
    target = "https://www.foo.com/"
    assert validator(current, target) is False

    current = "http://www.foo.com/bar"
    target = "https://www.foo.com/woo"
    assert validator(current, target) is False


def test_strip_fragment_identifier():
    base = "http://www.foo.com:8090/foo/bar/index.html#foo"
    defragged = ut.strip_fragment_identifier(base)
    assert defragged == "http://www.foo.com:8090/foo/bar/index.html"


def test_strip_fragment_identifier_does_not_mangle_if_no_frag():
    base = "http://www.foo.com:8090/foo/bar/index.html?q=34&b=12"
    defragged = ut.strip_fragment_identifier(base)
    assert defragged == "http://www.foo.com:8090/foo/bar/index.html?q=34&b=12"
