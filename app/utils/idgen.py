import uuid
def idgen() -> str:
    # Generate a random UUID string
    return str(uuid.uuid4().hex)