# -- Project information -----------------------------------------------------

project = "¥¢¢ Brain Log"
copyright = "2023, Jens W. Klein"
author = "Jens W. Klein"

# -- General configuration ---------------------------------------------------

exclude_patterns = ["venv/**"]
keep_warnings = True

extensions = [
    "ablog",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_favicon",
    "sphinx_togglebutton",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.youtube",
]

# -- Theme Options ----------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_title = project
html_theme_options = {
    "show_prev_next": False,
    "icon_links": [
        {
            # Label for this link
            "name": "Klein and Partner KG - My Company Website",
            # URL where the link will redirect
            "url": "https://kleiundpartner.at/",  # required
            # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "icon": "fa fa-globe",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        },
        {
            # Label for this link
            "name": "GitHub",
            # URL where the link will redirect
            "url": "https://github.com/jensens/",  # required
            # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "icon": "fa-brands fa-square-github",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        },
        {
            # Label for this link
            "name": "Mastodon",
            # URL where the link will redirect
            "url": "https://nerdculture.de/@jensens/",  # required
            # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "icon": "fa-brands fa-mastodon",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        },
    ],
}
html_sidebars = {
    "*": [
        "ablog/categories.html",
        "ablog/languages.html",
        "ablog/archives.html",
    ],
    "impress": [],
    "blog/*": [
        "ablog/postcard.html",
        "ablog/recentposts.html",
        "ablog/categories.html",
        "ablog/languages.html",
        "ablog/archives.html",
    ],
    "list/*": [
        "ablog/tagcloud.html",
        "ablog/categories.html",
        "ablog/languages.html",
        "ablog/archives.html",
    ],
}


# -- ABlog Options ----------------------------------------------------

blog_title = project
blog_baseurl = "https://yenzenz.com"
blog_authors = {
    "Jens W. Klein": ("Jens W. Klein", None),
}
blog_feed_archives = True
blog_path = "list"
post_date_format = "%Y-%m-%d"
post_date_format_short = "%Y-%m-%d"
blog_languages = {
    "en": ("English", None),
    "de": ("German", None),
}
post_show_prev_next = False
fontawesome_included=True
