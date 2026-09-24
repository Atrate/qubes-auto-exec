# Qubes Auto Exec

[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.en.html) 

## Description

This script is designed for QubesOS. It watches for startups of VMs with their
names defined as TOML table (section) headings and executes shell commands
specified in `start-#` variables. The variables can be single or multi-line
strings. The commands are executed sequentially based on the order they are
defined in the config file.

The `{vm.name}` placeholder is supported and will dynamically be replaced with
the VM's name when executed (that functionality will be more useful if anything
on the roadmap gets implemented).

The config file name path is hardcoded as `/etc/qubes/auto-exec.toml`.

## Usage

1. Download `qubes-auto-exec.py` and `qubes-auto-exec.service` and copy them over to `dom0`
2. Inside `dom0` copy the service file to `/etc/systemd/system` and the Python script to `/usr/local/bin`
3. Inside `dom0`, create `auto-exec.toml` in `/etc/qubes/` and modify it to suit your purposes (for examples, see section below)
4. Also inside `dom0`, execute `sudo chmod +x /usr/local/bin/qubes-auto-exec.py; sudo systemctl daemon-reload && sudo systemctl
   enable --now qubes-auto-exec`.

## Examples

The following example makes it so that a VM named `syncthing` will automatically
(via @rapenne-s's [NAT script, as modified by
me](https://forum.qubes-os.org/t/qubes-os-4-2-easily-nat-qubes-port-to-external-network/24958/24))
forward ports to `syncthing`.

```
[syncthing]
start-1 = "/usr/local/bin/nat.sh {vm.name} 22000 tcp"
start-2 = "/usr/local/bin/nat.sh {vm.name} 22000 udp"
start-3 = "/usr/local/bin/nat.sh {vm.name} 21027 udp -b"
```

## Security

For now, I don't believe there's a way for an AppVM to cause security issues
with this functionality, unless the user writes an insecure command themself.
With placeholder substitution a rogue VM with access to the Admin API could
possibly create a VM with a name that injects commands through `vm.name` but a)
that would require at least one of the roadmap items below to be implemented and
b) you'd probably have worse problems at this point.

## Roadmap

The following would be nice-to-have features, but unless I find them really
useful for myself, I won't be spending time developing them. PRs welcome.

1. Make it possible to match via globbing or regex.
2. Make it possible to match via VM tags or types.
3. Add more events, like on VM shutdown or pause/unpause.

## Credits

Part of the structure of the script is inspired by @noskb and @renehoj's CPU pinning script.

## Other Utilities

See [the qubes-utils repo](https://github.com/Atrate/qubes-utils) for links to other utilities I've written for Qubes.

## License
This project is licensed under the [AGPL-3.0-or-later](https://www.gnu.org/licenses/agpl-3.0.html).

[![License: AGPLv3](https://www.gnu.org/graphics/agplv3-with-text-162x68.png)](https://www.gnu.org/licenses/agpl-3.0.html)
