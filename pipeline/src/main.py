import os
import json
import subprocess
from pathlib import Path
from scanners import generate_sbom, analyze_dependencies, scan_code
from github_client import get_org_repos, clone_repo


ORG = "EbookFoundation"
DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
REPOS_DIR = DATA_DIR / "repos"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def main(skip_existing: bool = True):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPOS_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Obteniendo repos de {ORG}...")
    repos = get_org_repos(ORG, GITHUB_TOKEN)
    print(f"Encontrados {len(repos)} repos")
    
    for repo in repos:
        name = repo["name"]
        print(f"Procesando {name}...")
        
        repo_path = clone_repo(repo["clone_url"], str(REPOS_DIR))
        if not repo_path:
            continue
            
        sbom = generate_sbom(repo_path, str(DATA_DIR), skip_existing)
        if sbom:
            packages = sbom.get("artifacts", [])
            print(f"  SBOM: {len(packages)} paquetes")
        else:
            print(f"  SBOM: error")
        
        sca = analyze_dependencies(repo_path, str(DATA_DIR), skip_existing)
        if sca:
            vulns = sca.get("matches", [])
            print(f"  SCA: {len(vulns)} vulnerabilidades")
        else:
            print(f"  SCA: sin vulnerabilidades")
        
        sast = scan_code(repo_path, str(DATA_DIR), skip_existing)
        if sast:
            findings = sast.get("results", [])
            print(f"  SAST: {len(findings)} hallazgos")
        else:
            print(f"  SAST: sin hallazgos")
    
    print("Completado.")


if __name__ == "__main__":
    main()