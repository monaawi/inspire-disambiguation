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

"""Disambiguation extension."""

from __future__ import absolute_import, division, print_function

import os

from . import config


class BeardConfig(object):
    """Simple config manager available from whole app.

    It's a simple singleton so it will initialize only once.
    Default values are set in `set_default_values` method.
    Configuration is loaded from `config.py` located in the same folder as this file.
    Additionally all environment variables which name starts with `DISAMBIGUATION_`
        prefix will be loaded and will overwrite current values.
    `DISAMBIGUATION_` prefix will be removed from env values when loaded.

    Example:
        $ export DISAMBIGUATION_ES_HOSTNAME = "localhost:9201"
        $ python
        >>> from inspire_disambiguation import conf
        >>> conf['ES_HOSTNAME']
        "localhost:9201"

    """

    config_data = None
    instance_path = os.path.dirname(os.path.abspath(__file__))
    KEY_PREFIX = "DISAMBIGUATION_"

    def __new__(cls):
        if cls.config_data is not None:
            return cls.config_data
        else:
            cls.config_data = {}
            cls.init_config()
            return cls.config_data

    @classmethod
    def init_config(cls):
        cls.set_default_values()
        cls.read_config_from_module()
        cls.read_config_from_env()

    @classmethod
    def set_default_values(cls):
        disambiguation_base_path = os.path.join(cls.instance_path, "disambiguation")
        cls.config_data["BASE_PATH"] = disambiguation_base_path
        cls.config_data["CURATED_SIGNATURES_PATH"] = os.path.join(
            disambiguation_base_path, "curated_signatures.jsonl"
        )
        cls.config_data["INPUT_CLUSTERS_PATH"] = os.path.join(
            disambiguation_base_path, "input_clusters.jsonl"
        )
        cls.config_data["SAMPLED_PAIRS_PATH"] = os.path.join(
            disambiguation_base_path, "sampled_pairs.jsonl"
        )
        cls.config_data["PUBLICATIONS_PATH"] = os.path.join(
            disambiguation_base_path, "publications.jsonl"
        )
        cls.config_data["ETHNICITY_DATA_PATH"] = os.path.join(
            disambiguation_base_path, "ethnicity.csv"
        )
        cls.config_data["ETHNICITY_MODEL_PATH"] = os.path.join(
            disambiguation_base_path, "ethnicity.pkl"
        )
        cls.config_data["DISTANCE_MODEL_PATH"] = os.path.join(
            disambiguation_base_path, "distance.pkl"
        )
        cls.config_data["CLUSTERING_MODEL_PATH"] = os.path.join(
            disambiguation_base_path, "clustering.pkl"
        )
        cls.config_data["CLUSTERING_N_JOBS"] = 8
        cls.config_data["DISPLAY_PROGRESS"] = False
        cls.config_data["LOG_LEVEL"] = "WARNING"
        cls.config_data["REDIS_PHONETIC_BLOCK_KEY"] = "author_phonetic_blocks"

    @classmethod
    def read_config_from_module(cls):
        for k in dir(config):
            if k.isupper() and not k.startswith("__"):
                cls.config_data[k] = getattr(config, k)

    @classmethod
    def read_config_from_env(cls):
        for key, value in os.environ.items():
            if key.startswith(cls.KEY_PREFIX):
                cls.config_data[key[len(cls.KEY_PREFIX) :]] = value
