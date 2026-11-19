#!/usr/bin/env bash
# Tests supabase/schema.sql on a throwaway local Postgres. Needs Postgres 15 or newer installed.
# Usage: tests/sql/run.sh   (run as root on Linux, it switches to the "postgres" user)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
bin="$(ls -d /usr/lib/postgresql/*/bin | sort -V | tail -1)"
work="$(mktemp -d)"
cp "$here/stub.sql" "$here/test.sql" "$here/../../supabase/schema.sql" "$work/"
chmod -R a+rX "$work"; chown -R postgres "$work"
as_pg() { su postgres -s /bin/bash -c "$1"; }
as_pg "$bin/initdb -D $work/db -A trust >/dev/null"
as_pg "$bin/pg_ctl -D $work/db -o '-p 54329 -c listen_addresses= -k $work' -l $work/log -w start >/dev/null"
trap 'as_pg "$bin/pg_ctl -D $work/db -m immediate stop >/dev/null" || true; rm -rf "$work"' EXIT
q() { as_pg "PGOPTIONS=--client-min-messages=warning psql -X -q -v ON_ERROR_STOP=1 -h $work -p 54329 -d postgres $1"; }
q "-f $work/stub.sql"
q "-f $work/schema.sql"
q "-f $work/schema.sql"   # second run proves the file is safe to run again
q "-f $work/test.sql" 2>&1 | sed 's/^psql:[^ ]* NOTICE:  //'
