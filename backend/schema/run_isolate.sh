#!/bin/bash
export PAGER=cat
echo 'Poplu01@#' | sudo -S -u postgres psql -t -A -c "REVOKE ALL ON DATABASE trustcapture_db FROM nyaya_app;" 2>/dev/null
echo 'Poplu01@#' | sudo -S -u postgres psql -t -A -c "REVOKE ALL ON DATABASE trustcapture_test FROM nyaya_app;" 2>/dev/null
echo 'Poplu01@#' | sudo -S -u postgres psql -t -A -c "REVOKE ALL ON DATABASE test_trustcapture FROM nyaya_app;" 2>/dev/null
echo "DONE: nyaya_app isolated from trustcapture databases"
