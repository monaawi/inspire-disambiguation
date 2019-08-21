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
from unittest.mock import MagicMock

import numpy

from inspire_disambiguation.api import (
    train_and_save_ethnicity_model,
    process_clustering_output,
)
import os

from inspire_disambiguation.core.ml.models import Signature, Publication

ETHNICITY_TRAINING_DATA = """\
RACE,NAMELAST,NAMEFRST
1,Doe,John
2,Lee,Stan
3,Abdullah,FOO
4,Montana,Hannah
5,Doe,Jane
"""


def test_train_and_save_ethnicity_model(tmpdir):
    ethnicity_data_path = tmpdir.join("ethnicity.csv")
    ethnicity_data_path.write(ETHNICITY_TRAINING_DATA)
    ethnicity_model_path = tmpdir.join("ethnicity.pkl")
    train_and_save_ethnicity_model(ethnicity_data_path, ethnicity_model_path)
    assert os.path.getsize(ethnicity_model_path) > 0


def test_process_clustering_output_signatures_without_author_id():
    clusterer_mock = MagicMock()
    clusterer_mock.clusterer.labels_ = numpy.array([1, 1])
    clusterer_mock.X = numpy.array(
        [
            [
                Signature(
                    author_affiliation="Rutgers U., Piscataway",
                    author_id=None,
                    author_name="Doe, John",
                    publication=Publication(
                        abstract="Many curated authors",
                        authors=[
                            "Doe, John",
                            "Doe, J",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Jamie",
                            "Jamie",
                        ],
                        collaborations=[],
                        keywords=["keyword"],
                        publication_id=1,
                        title="Title",
                        topics=["category"],
                    ),
                    signature_block="JOhn",
                    signature_uuid="94fc2b0a-dc17-42c2-bae3-ca0024079e52",
                )
            ],
            [
                Signature(
                    author_affiliation="Rutgers U., Piscataway",
                    author_id=None,
                    author_name="Doe, John",
                    publication=Publication(
                        abstract="Many curated authors",
                        authors=[
                            "Doe, John",
                            "Doe, J",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Jamie",
                            "Jamie",
                        ],
                        collaborations=[],
                        keywords=["keyword"],
                        publication_id=1,
                        title="Title",
                        topics=["category"],
                    ),
                    signature_block="JOhn",
                    signature_uuid="94fc2b0a-dc17-42c2-bae3-ca0024079e54",
                )
            ],
        ],
        dtype=object,
    )

    expected_output = {
        (1, "94fc2b0a-dc17-42c2-bae3-ca0024079e52"): [],
        (1, "94fc2b0a-dc17-42c2-bae3-ca0024079e54"): [],
    }

    output = process_clustering_output(clusterer_mock)
    assert output == expected_output


def test_process_clustering_output_signatures_multiple_author_id():
    clusterer_mock = MagicMock()
    clusterer_mock.clusterer.labels_ = numpy.array([0, 0, 1, 1, 1])
    clusterer_mock.X = numpy.array(
        [
            [
                Signature(
                    author_affiliation="Rutgers U., Piscataway",
                    author_id=1,
                    author_name="Doe, John",
                    publication=Publication(
                        abstract="Many curated authors",
                        authors=[
                            "Doe, John",
                            "Doe, J",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Jamie",
                            "Jamie",
                        ],
                        collaborations=[],
                        keywords=["keyword"],
                        publication_id=11,
                        title="Title",
                        topics=["category"],
                    ),
                    signature_block="JOhn",
                    signature_uuid="94fc2b0a-dc17-42c2-bae3-ca0024079e52",
                )
            ],
            [
                Signature(
                    author_affiliation="Rutgers U., Piscataway",
                    author_id=None,
                    author_name="Doe, John",
                    publication=Publication(
                        abstract="Many curated authors",
                        authors=[
                            "Doe, John",
                            "Doe, J",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Jamie",
                            "Jamie",
                        ],
                        collaborations=[],
                        keywords=["keyword"],
                        publication_id=12,
                        title="Title",
                        topics=["category"],
                    ),
                    signature_block="JOhn",
                    signature_uuid="94fc2b0a-dc17-42c2-bae3-ca0024079e53",
                )
            ],
            [
                Signature(
                    author_affiliation="Rutgers U., Piscataway",
                    author_id=3,
                    author_name="Doe, John",
                    publication=Publication(
                        abstract="Many curated authors",
                        authors=[
                            "Doe, John",
                            "Doe, J",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Jamie",
                            "Jamie",
                        ],
                        collaborations=[],
                        keywords=["keyword"],
                        publication_id=13,
                        title="Title",
                        topics=["category"],
                    ),
                    signature_block="JOhn",
                    signature_uuid="94fc2b0a-dc17-42c2-bae3-ca0024079e54",
                )
            ],
            [
                Signature(
                    author_affiliation="Rutgers U., Piscataway",
                    author_id=None,
                    author_name="Doe, John",
                    publication=Publication(
                        abstract="Many curated authors",
                        authors=[
                            "Doe, John",
                            "Doe, J",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Jamie",
                            "Jamie",
                        ],
                        collaborations=[],
                        keywords=["keyword"],
                        publication_id=14,
                        title="Title",
                        topics=["category"],
                    ),
                    signature_block="JOhn",
                    signature_uuid="94fc2b0a-dc17-42c2-bae3-ca0024079e55",
                )
            ],
            [
                Signature(
                    author_affiliation="Rutgers U., Piscataway",
                    author_id=5,
                    author_name="Doe, John",
                    publication=Publication(
                        abstract="Many curated authors",
                        authors=[
                            "Doe, John",
                            "Doe, J",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Doe, John",
                            "Jamie",
                            "Jamie",
                        ],
                        collaborations=[],
                        keywords=["keyword"],
                        publication_id=15,
                        title="Title",
                        topics=["category"],
                    ),
                    signature_block="JOhn",
                    signature_uuid="94fc2b0a-dc17-42c2-bae3-ca0024079e56",
                )
            ],
        ],
        dtype=object,
    )

    expected_output = {
        (11, "94fc2b0a-dc17-42c2-bae3-ca0024079e52"): [(1, True)],
        (12, "94fc2b0a-dc17-42c2-bae3-ca0024079e53"): [(1, False)],
        (13, "94fc2b0a-dc17-42c2-bae3-ca0024079e54"): [(3, True), (5, True)],
        (14, "94fc2b0a-dc17-42c2-bae3-ca0024079e55"): [(3, False), (5, False)],
        (15, "94fc2b0a-dc17-42c2-bae3-ca0024079e56"): [(3, True), (5, True)],
    }
    output = process_clustering_output(clusterer_mock)
    assert output == expected_output

