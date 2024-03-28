from export import create_export
import config


if __name__ == "__main__":
  create_export(config.OUT_DIR, config.EMAIL)
