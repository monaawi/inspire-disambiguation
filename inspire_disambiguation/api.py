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
# or submit itself to any jurisdiction

"""Disambiguation API."""

from __future__ import absolute_import, division, print_function

import numpy
from inspire_disambiguation import conf
from inspire_disambiguation.core.es.readers import get_signatures, get_input_clusters
from inspire_disambiguation.core.ml.sampling import sample_signature_pairs
from .core.ml.models import (
    Clusterer,
    DistanceEstimator,
    EthnicityEstimator,
)


def train_and_save_ethnicity_model(load_data_path, save_model_path):
    """Train the ethnicity estimator model and save it to disk."""
    estimator = EthnicityEstimator()
    estimator.load_data(load_data_path)
    estimator.fit()
    estimator.save_model(save_model_path)


def train_and_save_distance_model(
    load_ethnicity_path,
    save_distance_model_path,
    sampled_pairs_size,
):
    """Train the distance estimator model and save it to disk."""
    curated_signatures = get_signatures(curated_only=True)
    input_clusters = get_input_clusters(curated_signatures)
    pairs = [pair for pair in sample_signature_pairs(
        curated_signatures, input_clusters, sampled_pairs_size
    )]
    ethnicity_estimator = EthnicityEstimator()
    ethnicity_estimator.load_model(load_ethnicity_path)

    distance_estimator = DistanceEstimator(ethnicity_estimator)
    distance_estimator.load_data(
        curated_signatures,
        pairs,
        sampled_pairs_size
    )
    distance_estimator.fit()
    distance_estimator.save_model(save_distance_model_path)


def cluster(signatures, input_clusters):
    """Train the clustering model and get output."""
    ethnicity_estimator = EthnicityEstimator()
    ethnicity_estimator.load_model(conf['DISAMBIGUATION_ETHNICITY_MODEL_PATH'])

    distance_estimator = DistanceEstimator(ethnicity_estimator)
    distance_estimator.load_model(conf['DISAMBIGUATION_DISTANCE_MODEL_PATH'])

    clusterer = Clusterer(distance_estimator)
    clusterer.load_data(
        signatures,
        input_clusters,
    )
    clusterer.fit(n_jobs=conf['DISAMBIGUATION_CLUSTERING_N_JOBS'])
    return process_output(clusterer)


def process_output(clusterer):
    labels = clusterer.clusterer.labels_
    output = {}
    for label in numpy.unique(labels):
        signatures = clusterer.X[labels == label]
        author_id_by_cluster = set()
        for sig in signatures:
            author_id_by_cluster.add(sig[0]['author_id'])
        for sig in signatures:
            output[(
                sig[0].publication['publication_id'],
                sig[0]['signature_uuid']
            )] = [(
                author_id,
                True if sig[0]['author_id'] else False
            ) for author_id in author_id_by_cluster if author_id]
    return output
