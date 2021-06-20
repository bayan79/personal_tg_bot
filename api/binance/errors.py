from application.errors import Error, ErrorFactory


class BinanceError(Error):
    codes = {
        403: "the WAF Limit (Web Application Firewall) has been violated",
        429: "breaking a request rate limit",
        418: "an IP has been auto-banned for continuing to send requests after receiving 429 codes",
    }


class BinanceErrorFactory(ErrorFactory):
    base_error = BinanceError
