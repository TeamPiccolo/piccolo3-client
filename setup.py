# Copyright 2018- The Piccolo Team
#
# This file is part of piccolo3-client.
#
# piccolo3-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# piccolo3-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with piccolo3-client.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

setup(
    name = "piccolo3-client",
    namespace_packages = ['piccolo3'],
    packages = find_packages(),
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    include_package_data = True,
    install_requires = [
        'aiocoap',
        'pytz',
        'configobj',
    ],
    entry_points={
        'console_scripts': [
            'piccolo3-record = piccolo3.precord:main',
            'piccolo3-integration-times = piccolo3.ptimes:main',
            ],
    },

    # metadata for upload to PyPI
    author = "Magnus Hagdorn, Alasdair MacArthur, Iain Robinson",
    description = "Part of the piccolo3 system. This package provides the piccolo3 client",
    license = "GPL",
    url = "https://bitbucket.org/teampiccolo/piccolo3-client",
)
