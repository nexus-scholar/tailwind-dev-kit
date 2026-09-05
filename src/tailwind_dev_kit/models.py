from __future__ import annotations

from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


class Snippet(BaseModel):
    name: str  # e.g. 'html', 'react', 'vue'
    language: str  # e.g. 'html', 'jsx', 'vue'
    version: Optional[Any] = None  # e.g. '4.3'
    mode: Optional[str] = None  # 'light' or 'dark'
    supports_dark_mode: bool = False
    code: Optional[str] = None
    preview: Optional[str] = None


class Component(BaseModel):
    id: str
    uuid: str
    name: str
    slug: str
    product: str  # 'Marketing', 'Application UI', 'Ecommerce'
    category: str  # e.g. 'Page Sections', 'Elements'
    subcategory: str  # e.g. 'Hero Sections', 'Buttons'
    subcat_url: str
    downloadable: bool = False
    is_new: bool = False
    archived: bool = False
    image_credits_html: Optional[str] = None
    large_width: Optional[int] = None
    large_height: Optional[int] = None
    small_width: Optional[int] = None
    small_height: Optional[int] = None
    snippets: Dict[str, Snippet] = Field(default_factory=dict)  # key: e.g. 'html', 'react', 'vue'


class Subcategory(BaseModel):
    name: str
    slug: str
    category: str
    product: str
    url: str
    component_count: int = 0


class Template(BaseModel):
    model_config = {"extra": "allow"}

    id: Optional[Any] = None
    name: str
    slug: str
    type: Optional[str] = None
    url: str
    download_url: Optional[str] = None
    preview_url: Optional[str] = None
    demo_preview_url: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    technologies: List[Any] = Field(default_factory=list)
    technologies_summary: List[str] = Field(default_factory=list)
    local_archive: Optional[str] = None
    archive_size_kb: Optional[int] = None
    banner_image_url: Optional[str] = None
    screenshots: List[str] = Field(default_factory=list)
    local_screens_dir: Optional[str] = None
    local_banner_image: Optional[str] = None
    local_screenshots: List[str] = Field(default_factory=list)


class ScrapeManifest(BaseModel):
    scraped_at: str
    tailwind_version: str = "4.3"
    total_components: int
    total_templates: int
    products: List[str]
    components: List[Component]
    templates: List[Template]
