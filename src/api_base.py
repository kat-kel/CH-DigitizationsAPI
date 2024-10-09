import ural


class WrapperBase:
    def __init__(self) -> None:
        pass

    @staticmethod
    def strip_protocol(url: str) -> str:
        return ural.strip_protocol(url)

    @staticmethod
    def split_url(url: str) -> list[str]:
        url_without_protocol = ural.strip_protocol(url)
        return url_without_protocol.split("/")

    @staticmethod
    def get_tld(url: str) -> str:
        url_without_protocol = ural.strip_protocol(url)
        parts = url_without_protocol.split("/")
        if len(parts) > 1:
            return parts[0]

    @classmethod
    def check_url_tld(cls, url: str, tld: str) -> bool:
        if not ural.is_url(url):
            return False
        parsed_tld = cls.get_tld(url=url)
        if parsed_tld and parsed_tld == tld:
            return True
        else:
            return False
