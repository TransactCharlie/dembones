import dembones.urlvalidators as uv


def test_same_domain_validator_same_domain_same_protocol():
    validator = uv.same_domain
    current = "http://www.foo.com"
    target = "http://www.foo.com/bar"
    assert validator(current, target)


def test_same_domain_validator_same_domain_different_protocol():
    validator = uv.same_domain
    current = "http://www.foo.com"
    target = "https://www.foo.com/bar"
    assert validator(current, target)


def test_same_domain_validator_different_hostname():
    validator = uv.same_domain
    current = "http://www.foo.com"
    target = "https://www.zoo.com/bar"
    assert validator(current, target) is False


def test_same_domain_up_path_validator_same_domain_same_protocol():
    validator = uv.same_domain_up_path
    current = "http://www.foo.com"
    target = "http://www.foo.com/bar"
    assert validator(current, target)


def test_same_domain_up_path_validator_same_domain_different_protocol():
    validator = uv.same_domain_up_path
    current = "http://www.foo.com"
    target = "https://www.foo.com/bar"
    assert validator(current, target)


def test_same_domain_up_path_validator_different_hostname():
    validator = uv.same_domain_up_path
    current = "http://www.foo.com"
    target = "https://www.zoo.com/bar"
    assert validator(current, target) is False


def test_same_domain_up_path_validator_forbids_backwards_path():
    validator = uv.same_domain_up_path
    current = "http://www.foo.com/bar"
    target = "https://www.foo.com/"
    assert validator(current, target) is False

    current = "http://www.foo.com/bar"
    target = "https://www.foo.com/woo"
    assert validator(current, target) is False
