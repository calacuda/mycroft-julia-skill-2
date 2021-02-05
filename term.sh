#!/usr/bin/env bash
#tmux -L $1
TMUX_CALL="tmux -L $1 new-session -s $1 -n $1"
JULIA_TERM="$2 /opt/mycroft/skills/mycroft-julia-skill-2.calacuda/term.py"
#JULIA_TERM="$2 term.py"
#echo "$TERMINAL -e $TMUX_CALL $JULIA_TERM"
exec "$TERMINAL -e $TMUX_CALL $JULIA_TERM"
