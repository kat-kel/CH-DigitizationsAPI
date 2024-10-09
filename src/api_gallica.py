from typing import Optional

import requests
from pydantic import BaseModel, Field, field_validator

from api_base import WrapperBase


class NotGallicaArKException(Exception):
    pass


class GallicaResult(BaseModel):
    ark: str = Field(alias="related")
    manifest_url: str = Field(alias="@id")
    description: str
    repository: list | Optional[str] = Field(alias="metadata")
    digitised_by: list | Optional[str] = Field(alias="metadata")
    source_images: list | Optional[str] = Field(alias="metadata")
    metadata_source: list | Optional[str] = Field(alias="metadata")
    shelfmark: list | Optional[str] = Field(alias="metadata")
    title: list | Optional[str] = Field(alias="metadata")
    date: list | Optional[str] = Field(alias="metadata")
    language: list | Optional[str] = Field(alias="metadata")
    format: list | str = Field(alias="metadata")
    catalogue_notice: list | Optional[str] = Field(alias="metadata")
    work_notice: list | Optional[str] = Field(alias="metadata")
    ensemble_notice: list | Optional[str] = Field(alias="metadata")

    @field_validator("ark")
    @classmethod
    def make_ark(cls, related: str):
        return related.removeprefix("https://gallica.bnf.fr/")

    @field_validator("repository")
    @classmethod
    def get_repository(cls, metadata: list) -> str | None:
        for m in metadata:
            if m["label"] == "Repository" and m["value"] and m["value"] != "":
                return m["value"]

    @field_validator("digitised_by")
    @classmethod
    def get_digitised_by(cls, metadata: list) -> str | None:
        for m in metadata:
            if m["label"] == "Digitised by":
                return m["value"]

    @field_validator("source_images")
    @classmethod
    def get_source_images(cls, metadata: list) -> str | None:
        for m in metadata:
            if m["label"] == "Source Images":
                return m["value"]

    @field_validator("metadata_source")
    @classmethod
    def get_metadata_source(cls, metadata: list) -> str | None:
        for m in metadata:
            if m["label"] == "Metadata Source":
                return m["value"]

    @field_validator("shelfmark")
    @classmethod
    def get_shelfmark(cls, metadata: list) -> str | None:
        for m in metadata:
            if m["label"] == "Shelfmark":
                return m["value"]

    @field_validator("title")
    @classmethod
    def get_title(cls, metadata: list) -> str | None:
        for m in metadata:
            if m["label"] == "Title":
                return m["value"]

    @field_validator("date")
    @classmethod
    def get_date(cls, metadata: list) -> str | None:
        """Ignore dates in Gallica that are a list of estimates."""
        for m in metadata:
            if m["label"] == "Date":
                if isinstance(m["value"], list) and len(m["value"]) == 1:
                    return m["value"]
                elif isinstance(m["value"], str):
                    return m["value"]

    @field_validator("language")
    @classmethod
    def get_language(cls, metadata: list) -> str | None:
        for m in metadata:
            if m["label"] == "Language":
                return m["value"]

    @field_validator("format")
    @classmethod
    def get_format(cls, metadata: list) -> list:
        for m in metadata:
            if m["label"] == "Format":
                if isinstance(m["value"], list):
                    return [v["@value"] for v in m["value"]]
                else:
                    return m["value"]

    @field_validator("ensemble_notice")
    @classmethod
    def get_ensemble_notice(cls, metadata: list) -> str | None:
        for m in metadata:
            if m["label"] == "Relation" and m["value"].startswith("Notice d'ensemble"):
                return m["value"].removeprefix("Notice d'ensemble : ")

    @field_validator("work_notice")
    @classmethod
    def get_work_notice(cls, metadata: list) -> str | None:
        for m in metadata:
            if m["label"] == "Relation" and m["value"].startswith("Notice d’oeuvre"):
                return m["value"].removeprefix("Notice d’oeuvre : ")

    @field_validator("catalogue_notice")
    @classmethod
    def get_catalogue_notice(cls, metadata: list) -> str | None:
        for m in metadata:
            if m["label"] == "Relation" and m["value"].startswith(
                "Notice du catalogue"
            ):
                return m["value"].removeprefix("Notice du catalogue : ")


class Gallica(WrapperBase):
    base = "https://gallica.bnf.fr/iiif/"
    tld = "gallica.bnf.fr"

    @classmethod
    def build_images_url(cls, ark: str) -> str:
        return cls.base + ark

    @classmethod
    def build_iiif_manifest(cls, ark: str) -> str:
        return cls.build_images_url(ark) + "/manifest.json"

    @classmethod
    def get_ark(cls, url: str) -> str:
        shortened_url = cls.strip_protocol(url)
        ark = shortened_url.removeprefix(cls.tld + "/")
        if not ark.startswith("ark:/12148"):
            raise NotGallicaArKException(ark)
        else:
            return ark

    @classmethod
    def is_url(cls, url: str) -> bool:
        """Confirms if the url is from Gallica.

        Examples:
            >>> irht_url = "https://arca.irht.cnrs.fr/ark:/63955/md655d86p718"
            >>> gallica_url = "https://gallica.bnf.fr/ark:/12148/btv1b53000321m"
            >>> Gallica.is_url(irht_url)
            False
            >>> Gallica.is_url(gallica_url)
            True

        Args:
            url (str): URL to test.

        Returns:
            bool: True if the URL is from Gallica.
        """
        return cls.check_url_tld(url=url, tld=cls.tld)

    @classmethod
    def object(cls, ark: str) -> GallicaResult:
        """_summary_

        Example:
            >>> ark = 'ark:/12148/btv1b53000321m'
            >>> obj = Gallica.object(ark=ark)
            >>> obj.ark
            'ark:/12148/btv1b53000321m'
            >>> obj.format
            'Papier et parchemin. - 112 feuillets. - 210 × 145 mm. - Reliure maroquin olive'

        Args:
            ark (str): ARK for the digitized document.

        Raises:
            NotGallicaArKException: The ARK is not from Gallica.

        Returns:
            GallicaResult: The API result validated and modeled in a Pydantic class.
        """
        if not ark.startswith("ark:/12148/"):
            raise NotGallicaArKException(ark)
        iiif_manifest = cls.build_iiif_manifest(ark=ark)
        json_response = requests.get(iiif_manifest).json()
        model = GallicaResult.model_validate(json_response)
        return model
