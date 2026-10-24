
SEARCH_REGISTRY={}

def register_search(platform: str):
    def decorator(fn):
        SEARCH_REGISTRY[platform] = fn
        return fn
    return decorator