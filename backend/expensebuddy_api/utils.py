import uuid
from db import get_group_byuser


def user_already_in_group(user_id, group_id):
    groups=get_group_byuser(user_id)
    if groups is not None and len(groups)>0:
        return uuid.UUID(group_id) in [group['id'] for group in groups]
    return False