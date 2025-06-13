#!/bin/bash
set -e
PM=1
DEV=1
while [[ $# -gt 0 ]]; do
  case $1 in
    --pm)
      PM="$2"
      shift 2
      ;;
    --dev)
      DEV="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done
SESSION=swarm

tmux new-session -d -s "$SESSION" -n orchestrator "python app/api/main.py"
tmux select-pane -t "$SESSION":0.0 -T "orchestrator"

for p in $(seq 1 "$PM"); do
  pm_win="pm${p}"
  tmux new-window -t "$SESSION" -n "$pm_win" "python app/agents/pm_agent.py --id ${p}"
  tmux select-pane -t "$SESSION":${pm_win}.0 -T "PM${p}"
  for d in $(seq 1 "$DEV"); do
    tmux split-window -t "$SESSION":${pm_win} -v "python app/agents/dev_agent.py --id ${p}-${d}"
    tmux select-pane -T "PM${p}-${d}"
    tmux select-layout -t "$SESSION":${pm_win} tiled
  done
done

 tmux attach -t "$SESSION"
