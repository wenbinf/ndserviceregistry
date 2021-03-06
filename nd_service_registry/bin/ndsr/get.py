# Copyright 2013 Nextdoor.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'me@ryangeyer.com (Ryan J. Geyer)'

import json
import yaml
import logging

log = logging.getLogger(__name__)


class Get(object):

    def __init__(self, ndsr):
        """
        Initializer

        Args:
            ndsr: An object implementing nd_service_registry
        """
        self.__ndsr = ndsr

    def __process_node(self, node, data=False, recursive=False):
        """Converts a raw dictionary response from nd_service_registry into a
        condensed dictionary used for CLI output

        Args:
            node: A dictionary result from nd_service_registry.get
            data: A boolean indicating whether data should be included in the
            result
            recursive: A boolean indicating whether child nodes should be
            recursed

        Returns:
            A dictionary with a display friendly format.  Contains data or
            child nodes based on the provided arguments
        """
        output = {}
        output.update({node['path']: {}})

        if data:
            dataval = None
            if 'data' in node:
                dataval = node['data']
            output[node['path']].update({'data': dataval})

        if recursive:
            children = []
            if 'children' in node:
                for key, val in node['children'].iteritems():
                    child = self.__ndsr.get("%s/%s" % (node['path'], key))
                    children.append(
                        self.__process_node(child, data, recursive)
                    )
                output[node['path']].update({'children': children})

        return output

    def execute(self, argv, gflags):
        """Makes the appropriate nd_service_registry query for the provided
        path and returns a string in the
        requested format.

        Args:
            argv: The CLI arguments, used to determine the path
            gflags: A gflags object with parsed CLI flags

        Returns:
            A string in the specified format or "No output format selected"
        """

        path = '/'
        if len(argv) > 2:
            path = argv[2]

        log.info("Fetching %s from zookeeper" % path)
        result = self.__ndsr.get(path)
        output = self.__process_node(result, gflags.data, gflags.recursive)

        if gflags.outputformat == 'yaml':
            return yaml.safe_dump(output, default_flow_style=False)
        elif gflags.outputformat == 'json':
            return json.dumps(output, sort_keys=True, indent=4,
                              separators=(',', ': '))
        else:
            return "No output format selected"
