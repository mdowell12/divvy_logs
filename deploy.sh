scp /Users/mdowell12/Documents/divvy_logs/divvy_logs/secret.py matt@192.168.0.103:/home/matt/github/divvy_logs/divvy_logs/

ssh matt@192.168.0.103 << EOF
  cd ~/github/divvy_logs
  git reset --hard HEAD
  git pull origin master

  source ~/github/divvy_logs/venv/bin/activate
  pip install -r ~/github/divvy_logs/requirements.txt
EOF
