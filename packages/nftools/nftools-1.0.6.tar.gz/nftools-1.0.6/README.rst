=======
nftools
=======


.. image:: https://img.shields.io/pypi/v/nftools.svg
        :target: https://pypi.python.org/pypi/nftools

.. image:: https://img.shields.io/travis/akajimeagle/nftools.svg
        :target: https://travis-ci.com/akajimeagle/nftools

.. image:: https://readthedocs.org/projects/nftools/badge/?version=latest
        :target: https://nftools.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

A CLI for managing your solana nft collection.


* Free software: MIT license
* Documentation: https://nftools.readthedocs.io.


Requirements
-------------

- `python3.7`_ installed.

.. _python3.7: https://www.python.org/downloads/

- `solana-cli-tools`_ installed.

.. _solana-cli-tools: https://docs.solana.com/cli/install-solana-cli-tools

- `spl-token-cli`_ installed.

.. _spl-token-cli: https://spl.solana.com/token



READY
------


Create Whitelist Token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*Create whitelist token (0 decimals) and mint specified amount to your wallet.*

::

$ nftools create-whitelist-token


Take Holder Snapshot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*Take snapshot of active holders for specified collection.
Captures wallet address, nft token address, and nft token account address.
Save in your specified format (json, csv, xlsx)*

::

$ nftools snapshot


Get Hash List
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*Get list of nft token addresses for specified collection. Save in your specified format (json, csv, xlsx)*

::

$ nftools get-hash-list


Get Collection NFts Held
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*Get # of collection NFTs held by owner. Save in your specified format (json, csv, xlsx)*

::

$ nftools get-holders


WIP
-------


Get Collection Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

$ nftools get-metadata


TODO
-------


Collection Airdrop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

$ nftools airdrop-collection
