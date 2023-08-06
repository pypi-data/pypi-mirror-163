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

`solana-cli-tools`_ installed.

.. _solana-cli-tools: https://docs.solana.com/cli/install-solana-cli-tools

`spl-token-cli`_ installed.

.. _spl-token-cli: https://spl.solana.com/token



READY
------


Create Whitelist Token:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

$ nftools create-whitelist-token

Take Holder Snapshot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

$ nftools snapshot

Get Hash List (Mint List):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

$ nftools get-mints


Get Collection Holders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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


TEST
