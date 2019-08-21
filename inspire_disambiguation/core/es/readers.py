# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
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

"""Disambiguation core ES readers."""

from __future__ import absolute_import, division, print_function

from elasticsearch_dsl import Q, Search
from elasticsearch_dsl.connections import connections

from inspire_disambiguation import conf
from inspire_disambiguation.core.helpers import _build_signature, _build_publication

SIGNATURE_FIELDS = [
    'authors.affiliations.value',
    'authors.curated_relation',
    'authors.full_name',
    'authors.record',
    'authors.signature_block',
    'authors.uuid',
    'control_number',
]


class LiteratureSearch(Search):
    connection = connections.create_connection(
                hosts=[conf.get("ES_HOSTNAME", 'localhost:9200')],
                timeout=conf.get("ES_TIMEOUT", 60)
            )

    def __init__(self, **kwargs):
        super().__init__(
            using=kwargs.get('using', LiteratureSearch.connection),
            index=kwargs.get('index', "records-hep"),
            doc_type=kwargs.get('doc_type', "hep"),
        )


def build_literature_query(signature_block=None, only_curated=False):
    query = Q('match', _collections="Literature")
    if only_curated:
        query += Q('term', authors__curated_relation=True)
    if signature_block:
        query += Q('term', authors__signature_block__raw=signature_block)
    res = LiteratureSearch().query(
        'nested',
        path='authors',
        query=query
    ).params(
        size=9999
    )
    return res


def get_signatures(signature_block=None, curated=None):
    """Get all signatures from the ES which are maching specified signature_block.

    Yields:
        dict: a signature which is matching signature_block.

    """
    res=build_literature_query
    for record in res.scan():
        record = record.to_dict()
        publication_id = record.get('control_number')
        for author in record.get('authors'):
            if curated and not author.get('curated_relation'):
                continue
            if signature_block and author.get('signature_block') != signature_block:
                continue
            yield _build_signature(author, publication_id)


def get_all_publications():
    """Get all publications from the ES.

        Walks through all Literature records and collects all information
        that will be useful for ``BEARD`` during training and prediction.

        Yields:
            dict: a publication.

        """
    query = Q('match', _collections="Literature")
    res = LiteratureSearch().query(query)
    for record in res.scan():
        yield _build_publication(record.to_dict())
