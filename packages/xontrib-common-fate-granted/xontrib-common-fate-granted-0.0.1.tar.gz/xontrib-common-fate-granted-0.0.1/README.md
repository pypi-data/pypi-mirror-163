<p align="center">
Use <a href="https://granted.dev">Common Fate's Granted CLI tool</a> for switching AWS profiles in <a href="https://xon.sh/">Xonsh shell</a>
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/eppeters/xontrib-common-fate-granted" target="_blank">tweet</a>.
</p>

## Prerequisites

Install [Granted](https://granted.dev) and ensure the `assumego` command is in your path already (try `which assumego`).

## Installation

To install use pip:

```bash
xpip install xontrib-common-fate-granted
# or: xpip install -U git+https://github.com/eppeters/xontrib-common-fate-granted
```

## Usage

Load the plugin in your `.xonshrc`.

e.g.:

```
xontrib load common_fate_granted
```

You can use `assume` now, just like people who use boring old shells!

...

## Known issues

* Please file an issue if you encounter a bug!

...

## Credits

* This package was created with [xontrib template](https://github.com/xonsh/xontrib-template).
* This port was first documented by [Eddie Peters](https://github.com/eppeters) in a [blog post on dinogalactic.com](https://www.dinogalactic.com/using-common-fates-granted-cli-tool-for-aws-profiles-with-xonsh-shell.html)
