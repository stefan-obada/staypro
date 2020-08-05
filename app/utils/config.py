import os


def generate_config_path(platform, overwrite=False):
    root = os.getcwd()
    cfg_path = os.path.join(root,"config", platform + ".ini")

    if not os.path.isfile(cfg_path):
        raise Exception(f"Cannot found config file for platform {platform}")

    else:
        return cfg_path
