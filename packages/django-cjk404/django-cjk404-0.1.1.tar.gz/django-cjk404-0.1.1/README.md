# Managed 404 Pages with Redirects

![Thank You Page](./readme/404.png)

## Description

A Wagtail package which will give you ability to automatically log and create of redirects from within Wagtail admin panel. 


### Features

- Automatic "404 Not Found" HTTP Error Detection Following the Non-Existent Page Opening 
- Support for Redirects to [Wagtail Pages](https://docs.wagtail.io/en/stable/reference/pages/index.html)

### How It Works  

- `Regular Expression → Regular Expression` [currently in development]
- `Regular Expression → URL`
- `Regular Expression → Wagtail Page`
- `URL → URL`
- `URL → Wagtail Page`

### Repository inspired by / based on a fork of:
- [wagtail_managed404](https://wagtail-managed404.readthedocs.io/) - abandoned in 2018
- [django-regex-redirects](https://github.com/maykinmedia/django-regex-redirects).

Both projects were similar (one `Model` class and fairly uncomplicated `Middleware`), so the easiest thing was simply to combine them, and work onwards from this base. 
Below, you can see the classes comparison of those two.

| **Django Regex Redirects**      | **Wagtail Managed 404 (Cjk404)** |
|:---------------------------:|:----------------------------:|
| `class Redirect(models.Model)`                    | `class PageNotFoundEntry(models.Model)`                |
| • `old_path`                    | • `url`                     |
| • `new_path`             | • `redirect_to_url` or `redirect_to_page`                   |
| • `regular_expression`               | -                     |
| • `fallback_redirect`              | -                     |
| • `nr_times_visited`           | • `hits`                     |

### Testing ###
Test suites based on source packages are under construction. Some basic tests currently work ok.

### Dependencies
- wagtail.contrib.modeladmin (https://docs.wagtail.io/en/stable/reference/contrib/modeladmin/index.html)

This package is used for the admin panel itself.

## Screenshots

#### "All Redirects" in the Backend

!["All Redirects" in the Backend"](./readme/All%20Redirects.jpg)

#### "Edit Redirect" in the Backend 

!["Edit Redirect" in the Backend](./readme/Edit%20Redirect.jpg)

### Usage
0. Get the app from PyPI:
```pip install django-cjk404```


1. Add 'cjk404' to the INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'wagtail.contrib.modeladmin', # required dependency
    'cjk404'
    ...
]
```

2. Add the supplied middleware. You may also want to disable Wagtail's default ```RedirectMiddleware```:

```python
MIDDLEWARE = [
    'cjk404.middleware.PageNotFoundRedirectMiddleware',
    # "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]
```

3. Run the migrations:
```python
python manage.py migrate
```

4. Visit the Wagtail admin area. You should see any 404s recorded in the application, and you can add redirects to them. You can also add your own redirects, e.g. based on regexp.

## Development

### Utility scripts - testing
Assuming you have Django>=4.0 and Wagtail>=3.0 pip-installed in your virtual environment, you do not need to set up a new Django/Wagtail project to develop/test the app.

After you ```git clone``` the repository, use ```load_tests.py``` to call ```boot_django``` and then to execute the unit tests.

## Authors

- [Grzegorz Król](https://github.com/cjkpl)
- [Filip Woźniak](https://github.com/FilipWozniak)

## Github URL

### Old URL:
[https://github.com/cjkpl/dj-apps-cjk404](https://github.com/cjkpl/dj-apps-cjk404)

### New URL:
[https://github.com/cjkpl/django-cjk404](https://github.com/cjkpl/django-cjk404)

Please migrate your local repositories to the new URL by executing:
```
$ git remote set-url origin https://github.com/cjkpl/django-cjk404
```