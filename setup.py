import shutil
from pathlib import Path
from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize


exts = [
    Extension('app.http', [
        'app/http/v1/handlers/*.py',
        # 'app/http/v1/schemas/*.py',
    ]),
    Extension('app.services', [
        'app/services/*.py',
    ]),
    Extension('app.repos', [
        'app/repos/*.py',
    ]),
    Extension('app.models', [
        'app/models/*.py',
    ]),
    Extension('app.jobs', [
        'app/jobs/*.py',
    ]),
    Extension('app.settings', [
        'app/settings.py',
    ]),
    Extension('app.utils', [
        'app/utils.py',
    ]),
    Extension('app.main', [
        'app/main.py',
    ]),
]

class MyBuildExt(build_ext):
    def run(self):
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent

        target_dir = build_dir if not self.inplace else root_dir

        self.copy_file(Path('http') / '__init__.py', root_dir, target_dir)
        self.copy_file(Path('jobs') / '__init__.py', root_dir, target_dir)
        self.copy_file(Path('services') / '__main__.py', root_dir, target_dir)
        self.copy_file(Path('repos') / '__main__.py', root_dir, target_dir)

    def copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return

        shutil.copyfile(str(source_dir / path), str(destination_dir / path))

setup(
    name='app',
    ext_modules=cythonize(
        exts,
        compiler_directives={
            'always_allow_keywords': True
        },
        build_dir="build",
    ),
    zip_safe=False,
    # packages=['http', 'services', 'repos', 'jobs', 'models']
    packages=[],
    # cmdclass=dict(
    #     build_ext=MyBuildExt
    # ),
)
