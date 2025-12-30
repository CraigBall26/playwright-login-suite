INVALID_EMAIL_FORMATS = {
    "missing_at_symbol": "patriotsfakehudl.com",
    "double_at_symbol": "packers@@fakehudl.com",
    "missing_username": "@cowboys.com",
    "missing_domain": "steelers@",
    "missing_tld": "broncos@fakehudl",
    "leading_dot_in_domain": "chiefs@.fakehudl.com",
    "double_dot_in_domain": "raiders@fakehudl..com",
    "spaces_in_email": "san francisco49ers@fakehudl.com",
    "unicode_characters": "rams🏈@fakehudl.com",
}

INVALID_EMAIL_DOMAINS = {
    "bills@hudl",
    "saints@hudl.x",
    "falcons@fake..com",
    "texans@.fakehudl.com",
}

INVALID_EMAIL_DISALLOWED_CHARS = {
    "brady()@hudl.com",
    "moss[]@hudl.com",
    "kelce;@hudl.com",
    "watt,@hudl.com",
    "revis🔥@hudl.com",
}
