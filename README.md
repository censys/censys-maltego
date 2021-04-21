# Censys Maltego Integration

<!-- [![PyPI](https://img.shields.io/pypi/v/censys_maltego?color=orange)](https://pypi.org/project/censys_maltego/) -->
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/censys/censys-maltego)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Welcome to Censys transforms for Maltego! Now you can use Censys data to easily perform investigations, quickly search or discover assets, and evaluate your company's digital asset risk by identifying server misconfigurations and rogue services.

## Install

Installation requires a few pre-requisites:

- You will need a [Censys account](https://censys.io/register) and [API Key](https://censys.io/account/api)
- A working instance of [Maltego](https://www.maltego.com/downloads/). Any supported version will work, but the CE edition is limited in how many results can be returned to the graph.
- A working python3 installation. [Python 3.6+](https://www.python.org/downloads/) is currently supported.

```bash
$ pip install censys_maltego
$ canari create-profile censys_maltego
...
Successfully created censys_maltego.mtz. You may now import this file into Maltego.

INSTRUCTIONS:
-------------
1. Open Maltego.
2. Click on the home button (Maltego icon, top-left corner).
3. Click on 'Import'.
4. Click on 'Import Configuration'.
5. Follow prompts.
6. Enjoy!
```

Edit `~/.canari/censys_maltego.conf` to include your Censys API ID and Secret. Alternatively you can configure your Censys credentials with the `censys config` command.

## Resources

- [Censys Homepage](https://censys.io/)
- [Source](https://github.com/censys/censys-maltego)
- [Issue Tracker](https://github.com/censys/censys-maltego/issues)

## Contributing

All contributions (no matter how small) are always welcome.

## License

This software is licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)

- Copyright (C) 2021 Censys, Inc.
