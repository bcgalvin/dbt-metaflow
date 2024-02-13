# SPDX-FileCopyrightText: 2024-present Bryan Galvin <bcgalvin@gmail.com>
#
# SPDX-License-Identifier: MIT
import sys

if __name__ == "__main__":
    from dbt_metaflow.cli import dbt_metaflow

    sys.exit(dbt_metaflow())
