from polylith import alias


def test_parse_one_key_one_value_alias():
    res = alias.parse(["opencv-python=cv2"])

    assert res["opencv-python"] == ["cv2"]
    assert len(res.keys()) == 1


def test_parse_one_key_many_values_alias():
    res = alias.parse(["matplotlib=matplotlib, mpl_toolkits"])

    assert res["matplotlib"] == ["matplotlib", "mpl_toolkits"]
    assert len(res.keys()) == 1


def test_parse_many_keys_many_values_alias():
    res = alias.parse(["matplotlib=matplotlib, mpl_toolkits", "opencv-python=cv2"])

    assert res["matplotlib"] == ["matplotlib", "mpl_toolkits"]
    assert res["opencv-python"] == ["cv2"]

    assert len(res.keys()) == 2


def test_pick_alias_by_key():
    aliases = {"opencv-python": ["cv2"]}

    keys = {"one", "two", "opencv-python", "three"}

    res = alias.pick(aliases, keys)

    assert res == {"cv2"}


def test_pick_aliases_by_keys():
    aliases = {"opencv-python": ["cv2"], "matplotlib": ["mpl_toolkits", "matplotlib"]}

    keys = {"one", "two", "opencv-python", "matplotlib", "three"}

    res = alias.pick(aliases, keys)

    assert res == {"cv2", "mpl_toolkits", "matplotlib"}


def test_pick_aliases_by_case_insensitive_keys():
    aliases = {
        "opencv-python": ["cv2"],
        "PyJWT": ["jwt"],
        "Jinja2": ["jinja2"],
        "PyYAML": ["_yaml", "yaml"],
    }

    keys = {"one", "two", "jinja2", "pyyaml", "opencv-python", "pyjwt"}

    res = alias.pick(aliases, keys)

    assert res == {"cv2", "jinja2", "jwt", "_yaml", "yaml"}


def test_pick_aliases_by_keys_using_normalized_names():
    aliases = {
        "name_with_underscore": ["with_underscore"],
        "name-with-hyphen": ["with_hyphen"],
        "name.something": ["with_dot"],
    }

    keys = {"name-with-underscore", "name-with-hyphen", "name-something"}

    res = alias.pick(aliases, keys)

    assert res == {"with_underscore", "with_hyphen", "with_dot"}


def test_pick_empty_alias_by_keys():
    aliases = {}

    keys = {"one", "two", "opencv-python", "matplotlib", "three"}

    res = alias.pick(aliases, keys)

    assert res == set()
