#!/bin/bash

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

$here/uninstall.sh $@
$here/install.sh $@
