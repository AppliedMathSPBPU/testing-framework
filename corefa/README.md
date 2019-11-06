# Corefa

## Overview

Corefa is tool for computational resources management. 

### Basics

- Worker &mdash; particular machine, available for resource allocation.
- Resource &mdash; CPUs and GPUs group on worker.
- Job &mdash; computational task to **run** on resource.
- User &mdash; account entry able to run particular job on resource. 
Has it's own ID.

### Support list

#### Workers

#### Clients

## Installation

### Worker

#### Windows

1. Install OpenSSH like described 
[here](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse#installing-openssh-from-the-settings-ui-on-windows-server-2019-or-windows-10-1809).
2. (TODO) Change default OpenSSH shell from windows shell to UNIX shell:
   1. Install shell (via cygwin for example).
   2. Add it to OpenSSH via PowerShell
   ([docs](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_server_configuration#configuring-the-default-shell-for-openssh-in-windows)):
   ```
   New-ItemProperty -Path "C:\Windows\System32\OpenSSH" -Name DefaultShell -Value "C:\cygwin64\bin\sh.exe" -PropertyType String -Force
   ```
3. (TODO) Create access via keys.
4. [Add worker](#add-worker) from some client first time.

#### Slurm cluster

Just [add worker](#add-worker) from some client first time.

### Client (TODO)

#### Windows

#### Unix-like systems

## Usage 

#### Add workers

Run **add-worker.py** passing json worker config.
- Saves worker information on the client.
- Initializes corefa on worker if it has not been initialized before.

#### Allocate time slot of resource on worker (TODO)

#### Create job (TODO)

#### Pool results (TODO)
