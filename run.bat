@echo off

set PYTHON=C:\CustomProgram\Anaconda3\envs\vocab\python.exe
cd ./flask-backend
start cmd.exe /k %PYTHON% app.py
cd ..
cd ./vue-vocab
start cmd.exe /k npm run dev
start http://localhost:5173/