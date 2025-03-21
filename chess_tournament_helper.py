from controller import controller as ctrl
import os


def main(controller):
    controller.start()


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    main(ctrl.Controller(dir_path))
