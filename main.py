from exporter import Exporter
import config


def main():
  Exporter(config.OUT_DIR, config.EMAIL).run()


if __name__ == "__main__":
  main()
