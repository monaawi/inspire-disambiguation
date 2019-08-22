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

import click
from inspire_disambiguation import conf
from inspire_disambiguation.api import (
    train_and_save_ethnicity_model,
    train_and_save_distance_model
)
@click.group()
def cli():
    pass

@cli.group()
def train():
    pass


@train.command()
@click.option(
    '-l',
    '--load',
    'load_data_path',
    default=conf['DISAMBIGUATION_ETHNICITY_DATA_PATH'],
    help="Path to ethnicity csv file."
)
@click.option('-s', '--save', 'save_model_path', default=conf['DISAMBIGUATION_ETHNICITY_MODEL_PATH'], help="Path for saving ethnicity model.")
def ethnicity_model(load_data_path, save_model_path):
    click.secho("Starting ETHNICITY training.", fg='green', blink=True, bold=True)
    click.secho("This will take a while.")
    train_and_save_ethnicity_model(load_data_path, save_model_path)
    click.secho(f"Done. Model saved in {save_model_path}")


@train.command()
@click.option('-l', '--load', 'ethnicity_model_path', default=conf['DISAMBIGUATION_ETHNICITY_MODEL_PATH'], help="Path to ethnicity model obtained after training on ethnicity data.")
@click.option('-s', '--save', 'save_model_path', default=conf['DISAMBIGUATION_DISTANCE_MODEL_PATH'], help="Path for saving distance model.")
@click.option('-p', '--pairs_size', 'sampled_pairs_size', default=conf['DISAMBIGUATION_SAMPLED_PAIRS_SIZE'], help="Size of sampled pairs. Has to be multiple of 12.")
def distance_model(ethnicity_model_path, save_model_path, sampled_pairs_size):
    click.secho("Starting Distance training.", fg='green', blink=True, bold=True)
    train_and_save_distance_model(ethnicity_model_path, save_model_path, sampled_pairs_size)
    click.secho(f"Done. Model saved in {save_model_path}")
