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

import pytest
import json


class FakeHit(dict):
    def to_dict(self):
        return self


def load_es_record(filename):
    with open(f"tests/data/{filename}.json", "r") as f:
        record = json.load(f)
    return FakeHit(record)


@pytest.fixture(scope="function")
def es_record_with_2_curated_authors():
    record = load_es_record("374836")
    return record


@pytest.fixture(scope="function")
def es_record_with_curated_author():
    record = load_es_record("374837")
    return record


@pytest.fixture(scope="function")
def es_record_with_curated_author_and_no_recid():
    record = load_es_record("406190")
    return record


@pytest.fixture(scope="function")
def es_record_with_non_curated_author():
    record = load_es_record("421404")
    return record
