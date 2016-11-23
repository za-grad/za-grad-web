from urlparse import urlparse


class DomainResolverMiddleware(object):

    def process_request(self, request):
        path = request.build_absolute_uri()
        result = urlparse(path)
        domain_parts = result.netloc.split('.')
        subdomain = None
        if len(domain_parts) == 3:
            subdomain = domain_parts[0]
        request.subdomain = subdomain
