import re
from sys import stdout

from django import http
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.timezone import now

from .models import PageNotFoundEntry
from wagtail.core.models import Site

IGNORED_404S = getattr(settings, "IGNORED_404S", [r"^/static/", r"^/favicon.ico"])

DJANGO_REGEX_REDIRECTS_CACHE_KEY = "django-regex-redirects-regular"
DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY = "django-regex-redirects-regex"
DJANGO_REGEX_REDIRECTS_CACHE_TIMEOUT = 60


class PageNotFoundRedirectMiddleware:
    def __init__(self, response):
        self.response = response
        self.blacklist_url_patterns = [re.compile(string) for string in IGNORED_404S]

    def __call__(self, request):
        url = request.path
        if self._check_url_in_blacklist(url):
            return self.response(request)
        else:
            return self.handle_request(request)

    def _check_url_in_blacklist(self, url):
        return any(pattern.match(url) for pattern in self.blacklist_url_patterns)

    def updateHitCount(self, entry_id: int):
        entry = PageNotFoundEntry.objects.get(id=entry_id)
        entry.hits += 1
        entry.last_hit = now()
        entry.save()

    def host_with_protocol(self, request):
        http_host = request.META.get("HTTP_HOST", "")
        if http_host:
            if request.is_secure():
                http_host = f"https://{http_host}"
            else:
                http_host = f"http://{http_host}"
        return http_host

    def HttpRedirect301302(self, request, location, is_permanent=False):
        if not location:
            return self.response(request)

        http_host = self.host_with_protocol(request)

        if not (location.startswith("http") or location.startswith("https")):
            location = http_host + location
        if is_permanent:
            return HttpResponsePermanentRedirect(location)
        else:
            return HttpResponseRedirect(location)

    def handle_request(self, request):
        response = self.response(request)
        if response.status_code != 404:
            return response

        url = request.path
        site = Site.find_for_request(request)

        # find matching url in PageNotFoundEntry, and increase hit count

        full_path = request.get_full_path()

        redirects = cache.get(DJANGO_REGEX_REDIRECTS_CACHE_KEY)
        if redirects is None:
            redirects = list(PageNotFoundEntry.objects.all().values())
            cache.set(
                DJANGO_REGEX_REDIRECTS_CACHE_KEY,
                redirects,
                DJANGO_REGEX_REDIRECTS_CACHE_TIMEOUT,
            )

        # non-regexp to be attempted first (faster)
        for redirect in redirects:

            if redirect["url"] == full_path:
                self.updateHitCount(redirect["id"])

                return self.HttpRedirect301302(
                    request, redirect["redirect_to_url"], redirect["permanent"]
                )

            if settings.APPEND_SLASH and not request.path.endswith("/"):
                path_len = len(request.path)
                slashed_full_path = f"{full_path[:path_len]}/{full_path[path_len:]}"
                stdout.write(f"SFP: {slashed_full_path}")

                if redirect["url"] == slashed_full_path:
                    self.updateHitCount(redirect["id"])
                    return self.HttpRedirect301302(
                        request, redirect["redirect_to_url"], redirect["permanent"]
                    )

        # no match found, try regexp
        regular_expressions_redirects = cache.get(
            DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY
        )
        if regular_expressions_redirects is None:
            regular_expressions_redirects = list(
                PageNotFoundEntry.objects.filter(regular_expression=True).values()
            )
            cache.set(
                DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY,
                regular_expressions_redirects,
                DJANGO_REGEX_REDIRECTS_CACHE_TIMEOUT,
            )

        for redirect in regular_expressions_redirects:

            try:
                old_path = re.compile(redirect["url"], re.IGNORECASE)
            except re.error:
                continue

            if old_path.match(full_path):

                self.updateHitCount(redirect["id"])

                new_path = redirect["redirect_to_url"].replace("$", "\\")
                replaced_path = re.sub(old_path, new_path, full_path)
                return self.HttpRedirect301302(
                    request, replaced_path, redirect["permanent"]
                )

        if response.status_code == 404:
            if not PageNotFoundEntry.objects.filter(url=url, site=site).exists():
                PageNotFoundEntry.objects.create(site=site, url=url, hits=1)
        return response
