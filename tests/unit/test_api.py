# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2019 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from inspire_disambiguation.api import train_and_save_ethnicity_model
import os

ETHNICITY_TRAINING_DATA = '''\
RACE,NAMELAST,NAMEFRST
1,Doe,John
2,Lee,Stan
3,Abdullah,FOO
4,Montana,Hannah
5,Doe,Jane
'''


def test_train_and_save_ethnicity_model(tmpdir):
    ethnicity_data_path = tmpdir.join('ethnicity.csv')
    ethnicity_data_path.write(ETHNICITY_TRAINING_DATA)
    ethnicity_model_path = tmpdir.join('ethnicity.pkl')
    train_and_save_ethnicity_model(ethnicity_data_path, ethnicity_model_path)
    assert os.path.getsize(ethnicity_model_path) > 0
