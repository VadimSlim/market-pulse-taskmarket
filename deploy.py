from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
REPO='VadimSlim/market-pulse-taskmarket'
def run(args): subprocess.run(args,cwd=ROOT,check=True)
if __name__=='__main__':
    run(['gh','api','--method','POST','repos/'+REPO+'/pages','-f','build_type=workflow'])
    run(['gh','workflow','run','pages.yml','--repo',REPO])
