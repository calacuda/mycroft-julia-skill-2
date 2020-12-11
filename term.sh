#!/usr/bin/env bash
TMUX="tmux new-session -s $1 -n $1"
TERM="$2 /opt/mycroft/skills/mycroft-julia-skill-2.calacuda/term.py"
$TERMINAL -e $TMUX $TERM
