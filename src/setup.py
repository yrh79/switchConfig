from distutils.core import setup
import py2exe

pfw = dict(
    script = "switchConfig.py",
    icon_resources = [(1, "icon.ico")],
    dest_base = r"switchConfig")

zipfile = r"shardlib"

options = {"py2exe": {"compressed": 1,
                      "optimize": 2,
                      }
           }


setup(options = options,
        zipfile = zipfile,
        windows = [switchConfig],

      data_files=[(".",
                     ["icon.ico"]),
                  ],
)

