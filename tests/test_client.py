# Copyright (C) 2020, 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <https://www.gnu.org/licenses/>.

import logging
from unittest import mock

from gstore.client import Client
from gstore.models import Organization


def test_client_resolve_orgs():
    client = Client('secret')

    logger = logging.getLogger('gstore.client.test')
    client.logger = logger

    with mock.patch.object(logger, 'info') as mock_logger:
        orgs = client.resolve_orgs([])

        assert len(orgs) == 0
        mock_logger.assert_called_once_with(
            'Resolve organizations from provided configuration')


def test_client_resolve_repos():
    client = Client('secret')
    fake_org = Organization('fake_org')

    logger = logging.getLogger('gstore.client.test')
    client.logger = logger

    with mock.patch.object(logger, 'info') as mock_logger:
        repos = client.resolve_repos([], fake_org)

        assert len(repos) == 0
        mock_logger.assert_called_once_with(
            'Resolve repositories from provided configuration')

    with mock.patch.object(logger, 'error') as mock_logger:
        repos = client.resolve_repos([''], fake_org)

        assert len(repos) == 0
        mock_logger.assert_called_once_with(
            'Invalid repo pattern: "%s", skip resolving', '')

    with mock.patch.object(logger, 'error') as mock_logger:
        repos = client.resolve_repos(['a:b:c'], fake_org)

        assert len(repos) == 0
        mock_logger.assert_called_once_with(
            'Invalid repo pattern: "%s", skip resolving', 'a:b:c')

    with mock.patch.object(logger, 'error') as mock_logger:
        repos = client.resolve_repos(['a:'], fake_org)

        assert len(repos) == 0
        mock_logger.assert_called_once_with(
            'Invalid repo pattern: "%s", skip resolving', 'a:')

    repos = client.resolve_repos(['foo:bar'], fake_org)
    assert len(repos) == 0