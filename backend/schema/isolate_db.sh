#!/bin/bash
# Revoke nyaya_app access to trustcapture databases
echo 'Poplu01@#' | sudo -S -u postgres psql <<EOF
REVOKE CONNECT ON DATABASE trustcapture_db FROM nyaya_app;
REVOKE CONNECT ON DATABASE trustcapture_test FROM nyaya_app;
REVOKE CONNECT ON DATABASE test_trustcapture FROM nyaya_app;
REVOKE ALL ON DATABASE trustcapture_db FROM nyaya_app;
REVOKE ALL ON DATABASE trustcapture_test FROM nyaya_app;
REVOKE ALL ON DATABASE test_trustcapture FROM nyaya_app;
EOF
echo "Isolation complete"
