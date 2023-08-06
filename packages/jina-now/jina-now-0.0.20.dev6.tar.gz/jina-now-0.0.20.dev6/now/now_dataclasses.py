from dataclasses import dataclass
from typing import Dict, Optional

from now.constants import Apps, DatasetTypes, Qualities


@dataclass
class UserInput:
    app: Optional[Apps] = None

    # data related
    data: Optional[str] = None
    is_custom_dataset: Optional[bool] = None

    custom_dataset_type: Optional[DatasetTypes] = None
    dataset_name: Optional[str] = None
    dataset_url: Optional[str] = None
    dataset_path: Optional[str] = None
    # AWS related
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region_name: Optional[str] = None

    # model related
    quality: Optional[Qualities] = Qualities.MEDIUM

    # cluster related
    cluster: Optional[str] = None
    create_new_cluster: Optional[bool] = False
    deployment_type: Optional[str] = None
    secured: Optional[bool] = False
    owner_id: Optional[str] = None
    jwt: Optional[Dict[str, str]] = None

    # These attributes are added but is not in use
    additional_user: Optional[bool] = False
    email_ids: Optional[str] = None
