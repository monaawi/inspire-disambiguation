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

"""Disambiguation helpers."""
from inspire_utils.helpers import maybe_int
from inspire_utils.record import get_value


def _get_author_affiliation(author):
    return get_value(author, "affiliations.value[0]", default="")


def _get_author_id(author):
    return get_recid_from_ref(author.get("record"))


def get_recid_from_ref(ref_obj):
    """Retrieve recid from jsonref reference object.
    If no recid can be parsed, returns None.
    """
    if not isinstance(ref_obj, dict):
        return None
    url = ref_obj.get("$ref", "")
    return maybe_int(url.split("/")[-1])


def _get_authors(record):
    return get_value(record, "authors.full_name", default=[])
