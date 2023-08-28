from pydantic import BaseModel
from typing import List, TypedDict

from Models.api import NeedToken
# C01gGI0bakGok

# - TAGS -
class TagResponse(BaseModel):
    tagId: int
    tag: str

class CreateTagFields(BaseModel):
    tag: str
    
class AddTagsToImageFields(BaseModel):
    tags: List[int]

class TagInDatabase(BaseModel):
    tagId: int
    tag: str

# - SECTIONS -
class CreateSectionFields(BaseModel):
    section: str
    includedTags: List[TagResponse]

class SectionResponse(BaseModel):
    sectionId: int
    section: str
    includedTags: List[TagResponse]

class SectionInDatabase(BaseModel):
    sectionId: int
    section: str
    description: str
    cover: str
    coverId: int

class SectionWithAllInfoInDatabase(TypedDict):
    sectionId: int
    section: str
    tagId: int
    tag: str
    description: str
    cover: str
    coverId: int

class SectionWithAllInfo(TypedDict):
    sectionId: int
    section: str
    description: str
    cover: str
    coverId: int
    tags: List[TagInDatabase]

# - FOLDERS -
class FolderWithAllInfoInDatabase(TypedDict):
    folderId: int
    folder: str
    sectionId: int
    description: str
    cover: str
    coverId: int
    section: str
    tagId: int
    tag: str

class FolderWithAllInfo(TypedDict):
    folderId: int
    folder: str
    sections: List[SectionWithAllInfo]


# - IMAGES -
class ImageInDatabase(BaseModel):
    imageId: int
    image: str
    priority: int

class ImageWithAllInfoInDatabase(TypedDict):
    imageId: int
    image: str
    priority: int
    tagId: int
    tag: str
    sectionId: int
    section: str
    description: str
    cover: str
    coverId: int

class ImageWithAllInfo(TypedDict):
    imageId: int
    image: str
    priority: int
    tags: List[TagInDatabase]
    sections: List[SectionInDatabase]

class CreateImageFields(NeedToken):
    tags: List[int]