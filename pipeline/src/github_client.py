import os
import json
import subprocess
from pathlib import Path


def get_org_repos(org_name: str, token: str = None) -> list:
    """
    Obtiene la lista de repositorios de una organización de GitHub.
    
    Args:
        org_name: Nombre de la organización
        token: Token de GitHub opcional
        
    Returns:
        Lista de diccionarios con info de cada repositorio
    """
    cmd = ["curl", "-s", f"https://api.github.com/orgs/{org_name}/repos?per_page=100"]
    
    if token:
        cmd[1] = "-sHAuthorization: token {}".format(token)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    repos = json.loads(result.stdout)
    return [{"name": r["name"], "clone_url": r["clone_url"]} for r in repos]


def clone_repo(clone_url: str, target_dir: str, depth: int = 1) -> str:
    """
    Clona un repositorio con profundidad limitada.
    
    Args:
        clone_url: URL del repositorio
        target_dir: Directorio destino
        depth: Profundidad del clone (1 = solo último commit)
        
    Returns:
        Ruta del repositorio clonado o None si falla
    """
    repo_name = Path(clone_url).stem
    dest_path = os.path.join(target_dir, repo_name)
    
    if os.path.exists(dest_path):
        return dest_path
        
    try:
        subprocess.run(
            ["git", "clone", "--depth", str(depth), "--quiet", clone_url, dest_path],
            check=True,
            timeout=120
        )
        return dest_path
    except subprocess.TimeoutExpired:
        print(f"Timeout clonando {repo_name}")
        return None
    except Exception as e:
        print(f"Error clonando {repo_name}: {e}")
        return None