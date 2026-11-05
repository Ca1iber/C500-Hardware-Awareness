#!/usr/bin/env bash
set -uo pipefail

device_id="${1:-0}"

if ! command -v mx-smi >/dev/null 2>&1; then
  printf 'ERROR: mx-smi is not available in PATH.\n' >&2
  exit 1
fi

run_optional() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  if ! "$@"; then
    printf 'WARN: command unavailable or unsupported in this environment.\n' >&2
  fi
}

printf 'captured_at=%s\n' "$(date --iso-8601=seconds)"
printf 'hostname=%s\n' "$(hostname)"
printf 'device_id=%s\n' "$device_id"
run_optional mx-smi --version
run_optional mx-smi --summary -i "$device_id"
run_optional mx-smi --show-hwinfo -i "$device_id"
run_optional mx-smi --show-memory -i "$device_id"
run_optional mx-smi --show-clock -i "$device_id"
run_optional mx-smi --show-hbm-bandwidth -i "$device_id"
run_optional mx-smi --show-ap-usage -i "$device_id"
run_optional mx-smi sgpu --show-mode -i "$device_id"
run_optional mx-smi sgpu --show-sched-class -i "$device_id"
run_optional mx-smi sgpu --show-timeslice -i "$device_id"
run_optional mx-smi sgpu --show-remain -i "$device_id"

