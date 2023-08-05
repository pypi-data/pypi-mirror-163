import sys

from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

from codecs import open
from os import path, remove
import re


here = path.abspath(path.dirname(__file__))
package_name = 'BDPoisson1D'
version_file = path.join(here, package_name, '_version.py')
with open(version_file, 'rt') as f:
    version_file_line = f.read()
version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(version_re, version_file_line, re.M)
if mo:
    version_string = mo.group(1)
else:
    raise RuntimeError('Unable to find version string in %s.' % (version_file,))

readme_file = path.join(here, 'README.md')
with open(readme_file, encoding='utf-8') as f:
    long_description = f.read()

extensions = [
    Extension(
        'BDPoisson1D._helpers',
        ['BDPoisson1D/_helpers.pyx'],
        depends=['BDPoisson1D/_helpers.pxd'],
    ),
    Extension(
        'BDPoisson1D.FirstOrderLinear',
        ['BDPoisson1D/FirstOrderLinear.pyx'],
        depends=['BDPoisson1D/FirstOrderLinear.pxd'],
    ),
    Extension(
        'BDPoisson1D.FirstOrderNonLinear',
        ['BDPoisson1D/FirstOrderNonLinear.pyx'],
        depends=['BDPoisson1D/FirstOrderNonLinear.pxd'],
    ),
    Extension(
        'BDPoisson1D.DirichletLinear',
        ['BDPoisson1D/DirichletLinear.pyx'],
        depends=['BDPoisson1D/DirichletLinear.pxd'],
    ),
    Extension(
        'BDPoisson1D.DirichletNonLinear',
        ['BDPoisson1D/DirichletNonLinear.pyx'],
        depends=['BDPoisson1D/DirichletNonLinear.pxd'],
    ),
    Extension(
        'BDPoisson1D.NeumannLinear',
        ['BDPoisson1D/NeumannLinear.pyx'],
        depends=['BDPoisson1D/NeumannLinear.pxd'],
    ),
]

c_opt = {'msvc': [],
         'mingw32': [],
         'unix': []}
l_opt = {'mingw32': [],
         'unix': []}


# check whether compiler supports a flag
def has_flag(compiler, flag_name):
    import tempfile
    from distutils.errors import CompileError
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as file:
        file.write('int main (int argc, char **argv) { return 0; }')
        try:
            res = compiler.compile([file.name], extra_postargs=[flag_name])
            for item in res:
                remove(item)
        except CompileError:
            return False
    return True


# filter flags, returns list of accepted flags
def flag_filter(compiler, flags):
    result = []
    for flag in flags:
        if has_flag(compiler, flag):
            result.append(flag)
    return result


class CustomBuildExt(build_ext):
    def build_extensions(self):
        c = self.compiler.compiler_type
        print('Compiler:', c)
        opts = flag_filter(self.compiler, c_opt.get(c, []))
        linker_opts = flag_filter(self.compiler, l_opt.get(c, []))
        for e in self.extensions:
            e.extra_compile_args = opts
            e.extra_link_args = linker_opts
        build_ext.build_extensions(self)


setup(
    name=package_name,
    version=version_string,

    description='BD Finite Difference Poisson equation solver',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/bond-anton/BDPoisson1D',

    author='Anton Bondarenko',
    author_email='bond.anton@gmail.com',

    license='Apache Software License',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='FiniteDifference PDE Poisson',

    packages=find_packages(exclude=['demo', 'tests', 'docs', 'contrib', 'venv']),
    ext_modules=cythonize(extensions, compiler_directives={'language_level': sys.version_info[0]}),
    package_data={'BDPoisson1D': ['FirstOrderLinear.pxd', 'FirstOrderNonLinear.pxd',
                                  'DirichletLinear.pxd', 'DirichletNonLinear.pxd',
                                  'NeumannLinear.pxd',
                                  'Function.pxd', '_helpers.pxd']},
    install_requires=['numpy', 'scipy>=0.17.0', 'matplotlib', 'BDMesh>=0.2.18', 'BDFunction1D>=0.1.2'],
    cmdclass={'build_ext': CustomBuildExt},
)
