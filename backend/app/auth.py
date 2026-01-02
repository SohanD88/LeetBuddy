from fastapi import Header, HTTPException

def get_current_user_id(
    x_user_id: str | None = Header(default=None),
):
    """
    TEMP AUTH FOR V2.1 STEP 6

    Uses x-user-id header to simulate authentication.
    Allows testing user scoping without JWT complexity.
    """

    if not x_user_id:
        raise HTTPException(
            status_code=401,
            detail="Missing x-user-id header"
        )

    return x_user_id
