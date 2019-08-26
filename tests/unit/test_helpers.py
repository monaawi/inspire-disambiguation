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
from inspire_disambiguation.core.helpers import _get_author_affiliation, _get_author_id, get_recid_from_ref, \
    _get_authors, _build_publication, _build_signature
from inspire_disambiguation.core.ml.models import Signature, Publication


def test_get_author_affiliation(author):
    result = _get_author_affiliation(author)
    expected_result = "Rutgers U., Piscataway"
    assert result == expected_result


def test_get_author_id(author):
    result = _get_author_id(author)
    expected_result = 989441
    assert result == expected_result


def test_get_author_affiliation(author):
    result = _get_author_affiliation(author)
    expected_result = "Rutgers U., Piscataway"
    assert result == expected_result


def test_get_recid_from_ref_returns_none_on_none():
    assert get_recid_from_ref(None) is None


def test_get_recid_from_ref_returns_none_on_simple_strings():
    assert get_recid_from_ref('a_string') is None


def test_get_recid_from_ref_returns_none_on_empty_object():
    assert get_recid_from_ref({}) is None


def test_get_recid_from_ref_returns_none_on_object_with_wrong_key():
    assert get_recid_from_ref({'bad_key': 'some_val'}) is None


def test_get_recid_from_ref_returns_none_on_ref_a_simple_string():
    assert get_recid_from_ref({'$ref': 'a_string'}) is None


def test_get_recid_from_ref_returns_none_on_ref_malformed():
    assert get_recid_from_ref({'$ref': 'http://bad_url'}) is None


def test_get_recid_from_ref():
    assert get_recid_from_ref({'$ref': 'http://labs.inspirehep.net/api/authors/2'}) == 2


def test_get_authors(record):
    result = _get_authors(record)
    expected_result = ["Doe, John"]
    assert result == expected_result


def test_build_publication(record):
    result = _build_publication(record)
    expected_result = {
        'abstract': '2 curated authors with recid',
        'authors': ['Doe, John'],
        'collaborations': ["ATLAS"],
        'keywords': ['effective action', 'approximation: semiclassical'],
        'publication_id': 374836,
        'title': 'Title',
        'topics': ['Theory-HEP']
    }
    assert result == expected_result


def test_build_signature(author, record):
    result = _build_signature(author, record)
    expected_result = Signature(
        author_affiliation='Rutgers U., Piscataway', author_id=989441, author_name='Doe, John',
        publication=Publication(
            abstract='2 curated authors with recid', authors=['Doe, John'],
            collaborations=['ATLAS'],
            keywords=['effective action', 'approximation: semiclassical'],
            publication_id=374836, title='Title', topics=['Theory-HEP']
        ),
        signature_block='JOhn', signature_uuid='94fc2b0a-dc17-42c2-bae3-ca0024079e52'
    )
    assert result == expected_result
