def strtobool(x):
    try:
        b = x.lower() in ("true", "yes", "1", "y")
        return b
    except AttributeError:
        return False
    except NameError:
        return False