from typing import Optional

import requests
from pydantic import BaseModel, Field, field_validator

from api_base import WrapperBase


class NotIRHTArKException(Exception):
    pass


class IRHTManuscriptReproduction(BaseModel):
    ark_href: str = Field(alias="ark_href")
    ark: str = Field(alias="ark_href")
    manifest_url: Optional[str] = Field(alias="manifest_url")

    @field_validator("ark")
    @classmethod
    def make_ark(cls, ark_href: str) -> str:
        return ark_href.removeprefix("https://api.irht.cnrs.fr/reproductions/")


class IRHTManuscriptResult(BaseModel):
    id: int
    href: str
    ark_href: str
    ark: str
    notice_url: str = Field(alias="ark")
    shelfmark: dict | Optional[str]
    support: Optional[str]
    content: Optional[str]
    dimensions: Optional[str]
    nbpage: Optional[str]
    dating: Optional[str]
    alt_shelfmarks: Optional[list]
    illustrations: list
    languages: list
    related_links: list
    complete_reproduction: list | IRHTManuscriptReproduction = Field(
        alias="reproductions"
    )

    @field_validator("notice_url")
    @classmethod
    def construct_notice_url(cls, ark: str) -> str:
        return "https://arca.irht.cnrs.fr/" + ark

    @field_validator("shelfmark")
    @classmethod
    def get_shelfmark(cls, shelfmark: dict) -> str:
        return shelfmark["identifier"]

    @field_validator("alt_shelfmarks")
    @classmethod
    def get_alt_shelfmarks(cls, alt_shelfmarks: list) -> list:
        if not alt_shelfmarks:
            return []
        else:
            return [s["identifier"] for s in alt_shelfmarks]

    @field_validator("illustrations")
    @classmethod
    def get_illustrations(cls, illustrations: list) -> list:
        return [v["name"].strip() for v in illustrations]

    @field_validator("languages")
    @classmethod
    def get_languages(cls, languages: list) -> list:
        return [v["name"].strip() for v in languages]

    @field_validator("related_links")
    @classmethod
    def get_related_links(cls, related_links: list) -> list:
        links = []
        for link in related_links:
            source = link["title"]
            if source == "DEAF":
                ref = link["href"].split(".php#")[-1]
                links.append(f"DEAF:{ref}")
            else:
                ref = link["href"]
                links.append(f"{source}:{ref}")
        return links

    @field_validator("complete_reproduction")
    @classmethod
    def get_reproductions(
        cls, reproductions: list
    ) -> IRHTManuscriptReproduction | None:
        for r in reproductions:
            if r["subject"] == "intégral" and r["manifest_url"]:
                return IRHTManuscriptReproduction.model_validate(r)
            elif r["subject"] == "intégral":
                return IRHTManuscriptReproduction.model_validate(r)


class IRHT(WrapperBase):
    base = "https://api.irht.cnrs.fr/manuscripts/"
    tld = "arca.irht.cnrs.fr"

    @classmethod
    def build_url(cls, ark: str) -> str:
        """Build a URI to collect metadata on IRHT's manuscripts.

        Examples:
            >>> ark = 'ark:/63955/md11kh04f81h'
            >>> IRHT.build_url(ark=ark)
            'https://api.irht.cnrs.fr/manuscripts/ark:/63955/md11kh04f81h?mode=medium'

        Args:
            ark (str): ARK of a manuscript in IRHT's database.

        Returns:
            str: A URI for IRHT's manuscripts endpoint.
        """

        return cls.base + ark + "?mode=medium"

    @classmethod
    def is_url(cls, url: str) -> bool:
        """Confirms if the url is from IRHT.

        Examples:
            >>> irht_url = "https://arca.irht.cnrs.fr/ark:/63955/md655d86p718"
            >>> gallica_url = "https://gallica.bnf.fr/ark:/12148/btv1b53000321m"
            >>> IRHT.is_url(irht_url)
            True
            >>> IRHT.is_url(gallica_url)
            False

        Args:
            url (str): URL to test.

        Returns:
            bool: True if the URL is from IRHT.
        """

        return cls.check_url_tld(url=url, tld=cls.tld)

    @classmethod
    def get_ark(cls, url: str) -> str:
        shortened_url = cls.strip_protocol(url)
        ark = shortened_url.removeprefix(cls.tld + "/")
        if not ark.startswith("ark:/63955"):
            raise NotIRHTArKException(ark)
        else:
            return ark

    @classmethod
    def object(cls, ark: str) -> IRHTManuscriptResult:
        """From the manuscript's ARK, collect metadata from IRHT's API.

        Examples:
            >>> ark = 'ark:/63955/md268336h32b'
            >>> obj = IRHT.object(ark)
            >>> obj.id
            230
            >>> obj.complete_reproduction.manifest_url
            'https://api.irht.cnrs.fr/ark:/63955/fsvzptwicviq/manifest.json'


        Args:
            ark (str): ARK of a manuscript in IRHT's database, starting with "ark:/63955".

        Raises:
            NotIRHTArKException: The ARK is not from IRHT.

        Returns:
            IRHTManuscriptResult: The API result validated and modeled in a Pydantic class.
        """

        if not ark.startswith("ark:/63955/"):
            raise NotIRHTArKException(ark)
        url = cls.build_url(ark)
        json_response = requests.get(url).json()
        modeled_result = IRHTManuscriptResult.model_validate(json_response)
        return modeled_result
