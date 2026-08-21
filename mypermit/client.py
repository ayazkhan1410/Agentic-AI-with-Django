from django.conf import settings

from permit import Permit


def get_permit_client():
    pdp_url = settings.PERMIT_PDP_URL
    api_key = settings.PERMIT_API_KEY

    if not pdp_url or not api_key:
        raise ValueError("PERMIT_PDP_URL and PERMIT_API_KEY must be set")

    return Permit(
        pdp=pdp_url, token=api_key
    )


permit_client = get_permit_client()
