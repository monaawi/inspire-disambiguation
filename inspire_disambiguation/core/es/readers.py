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

from collections import defaultdict

import six
from elasticsearch_dsl import Q, Search
from elasticsearch_dsl.connections import connections

from inspire_disambiguation import conf
from inspire_disambiguation.core.helpers import _build_signature, _get_author_id


class LiteratureSearch(Search):
    connection = connections.create_connection(
                hosts=[conf["ES_HOSTNAME"]],
                timeout=conf.get("ES_TIMEOUT", 60)
            )

    def __init__(self, **kwargs):
        super().__init__(
            using=kwargs.get('using', LiteratureSearch.connection),
            index=kwargs.get('index', "records-hep"),
            doc_type=kwargs.get('doc_type', "hep"),
        )


def get_lit_records_query(signature_block=None, only_curated=False):
    SIGNATURE_FIELDS = [
        'abstracts.value',
        'affiliations.value',
        'authors.affiliations.value',
        'authors.curated_relation',
        'authors.full_name',
        'authors.record',
        'authors.signature_block',
        'authors.uuid',
        'control_number',
        'collaborations.value',
        'keywords.value',
        'titles.title',
        'inspire_categories.term',
    ]
    literature_query = Q('match', _collections="Literature")
    query_authors_helper = Q()
    if only_curated:
        query_authors_helper += Q('term', authors__curated_relation=True)
    if signature_block:
        query_authors_helper += Q('term', authors__signature_block__raw=signature_block)
    authors_query = Q('nested', path='authors', query=query_authors_helper)
    query = LiteratureSearch().query(
        Q('bool', must=[literature_query, authors_query])
    ).params(
        size=conf.get('ES_MAX_QUERY_SIZE', 9999),
        _source=SIGNATURE_FIELDS
    )
    return query


def get_signatures(signature_block=None, only_curated=False):
    """Get all signatures from the ES which are maching specified signature_block.

    Yields:
        dict: a signature which is matching signature_block.

    """
    query = get_lit_records_query(signature_block, only_curated)
    results = []
    for record in query.scan():
        record = record.to_dict()
        for author in record.get('authors'):
            if only_curated and not author.get('curated_relation'):
                continue
            if signature_block and author.get('signature_block') != signature_block:
                continue
            signature = _build_signature(author, record)
            if only_curated and not signature.get('author_id', None):
                continue
            results.append(signature)
    return results


def get_input_clusters(signatures):
    """Process signatures and return input clusters.
    Args:
        signatures: iterable of signatures.

    Returns:
        list: list of all input clusters for provided signatures.

    """
    input_clusters = []
    signatures_with_author = defaultdict(list)
    signatures_without_author = []
    for signature in signatures:
        if signature.get('author_id', None):
            signatures_with_author[signature['author_id']].append(
                signature['signature_uuid'])
        else:
            signatures_without_author.append(signature['signature_uuid'])
    cluster_id=0
    for cluster_id, (author_id, signature_uuids) in enumerate(six.iteritems(signatures_with_author)):
        input_clusters.append({
            'author_id': author_id,
            'cluster_id': cluster_id,
            'signature_uuids': signature_uuids,
        })
    for cluster_id, signature_uuid in enumerate(signatures_without_author, cluster_id + 1):
        input_clusters.append({
            'author_id': None,
            'cluster_id': cluster_id,
            'signature_uuids': [signature_uuid],
        })
    return input_clusters
