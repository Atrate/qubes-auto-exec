#!/usr/bin/env python3

import asyncio
import subprocess
import tomllib
import sys
import threading

import qubesadmin
import qubesadmin.events

# Threading helper
def run_cmds(vm_name, cmds, event):
    for key in cmds:
        # Only run on domain-start for start-* keys
        if event == "domain-start" and key.startswith("start-"):
            # Strip cmd and substitute {vm.name} string with var
            cmd = str(cmds[key]).strip().replace("{vm.name}", str(vm_name))
            try:
                print("Starting VM:", vm_name, "triggered command:", cmd)
                # Try also sending a notification to the user
                try: 
                    subprocess.run(["notify-send", "-a", "qubes-auto-exec", "-u", "low", f"""Starting VM: {vm_name} triggered command""", cmd], timeout=5)
                except Exception:
                    pass
                subprocess.run(cmd, shell=True).check_returncode()
            except subprocess.CalledProcessError as e:
                print("Error running command:", e)
    print("Done running commands for VM:", vm_name)

# Dispatch CMD chain for VM
def exec_dispatch(vm, event, **kwargs):
    vm = app.domains[str(vm)]

    # Return early if VM does not have a config table
    if vm.name not in config:
        return

    cmds = config[vm.name]
    threading.Thread(target=run_cmds, args=(vm.name, cmds, event), daemon=True).start()


# Open config file
try:
    configf = open("/etc/qubes/auto-exec.toml", "rb")
except Exception as e:
    print("Could not open config file:", e)
    sys.exit(1)
else:
    with configf:
        # Load TOML from config file
        try:
            config: dict = tomllib.load(configf)
        except Exception as e:
            print("Invalid TOML file:", e)
            sys.exit(1)
        else:
            # Listen on domain-start events and execute dispatch
            app = qubesadmin.Qubes()
            app.blind_mode = True
            dispatcher = qubesadmin.events.EventsDispatcher(app)
            dispatcher.add_handler('domain-start', exec_dispatch)
            asyncio.run(dispatcher.listen_for_events())
