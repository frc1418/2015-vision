#!/bin/sh

ROOTDIR="$(dirname "$(readlink -f "$0")")"
cd $ROOTDIR/../robot-vision

PIDFILE=/var/run/1418vision.pid
SCRIPT=run_one.sh

case "$1" in
  start)
    if [ -e $PIDFILE -a -e /proc/`cat $PIDFILE 2> /dev/null` ]; then
      echo "$0 already started"
      exit 1
    fi

    touch $PIDFILE
    chmod +r $PIDFILE
    chown lvuser $PIDFILE

    ./main.py -n --url http://localhost:5800/?action=stream &
    echo $! > $PIDFILE
    ;;
  stop)
    # kill saved PID
    if [[ -f "$PIDFILE" ]]; then
      kill `cat $PIDFILE`
      rm $PIDFILE
    fi
    ;;
esac
