import json
import subprocess
import os
from pathlib import Path


def generate_sbom(repo_path: str, output_dir: str, skip_existing: bool = True) -> dict:
    """
    Genera un SBOM usando Syft para un repositorio dado.
    """
    repo_name = Path(repo_path).name
    output_file = os.path.join(output_dir, f"sbom_{repo_name}.json")
    
    if skip_existing and os.path.exists(output_file):
        print(f"  SBOM: usando archivo existente")
        with open(output_file, 'r') as f:
            return json.load(f)
    
    try:
        result = subprocess.run(
            ["syft", "packages", "dir:" + repo_path, "-o", "json"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            sbom_data = json.loads(result.stdout)
            with open(output_file, 'w') as f:
                json.dump(sbom_data, f, indent=2)
            return sbom_data
        else:
            print(f"Error SBOM para {repo_name}: {result.stderr}")
            return {}
            
    except subprocess.TimeoutExpired:
        print(f"Timeout SBOM para {repo_name}")
        return {}
    except Exception as e:
        print(f"Excepción SBOM para {repo_name}: {e}")
        return {}


def analyze_dependencies(repo_path: str, output_dir: str, skip_existing: bool = True) -> dict:
    """
    Analiza vulnerabilidades en dependencias usando Grype (SCA).
    """
    repo_name = Path(repo_path).name
    output_file = os.path.join(output_dir, f"sca_{repo_name}.json")
    
    if skip_existing and os.path.exists(output_file):
        print(f"  SCA: usando archivo existente")
        with open(output_file, 'r') as f:
            return json.load(f)
    
    try:
        result = subprocess.run(
            ["grype", "dir:" + repo_path, "-o", "json"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            sca_data = json.loads(result.stdout)
            with open(output_file, 'w') as f:
                json.dump(sca_data, f, indent=2)
            return sca_data
        else:
            print(f"Error SCA para {repo_name}: {result.stderr}")
            return {}
            
    except subprocess.TimeoutExpired:
        print(f"Timeout SCA para {repo_name}")
        return {}
    except Exception as e:
        print(f"Excepción SCA para {repo_name}: {e}")
        return {}


def scan_code(repo_path: str, output_dir: str, skip_existing: bool = True) -> dict:
    """
    Escanea código fuente usando Semgrep (SAST).
    """
    repo_name = Path(repo_path).name
    output_file = os.path.join(output_dir, f"sast_{repo_name}.json")
    
    if skip_existing and os.path.exists(output_file):
        print(f"  SAST: usando archivo existente")
        with open(output_file, 'r') as f:
            return json.load(f)
    
    try:
        result = subprocess.run(
            ["semgrep", "scan", "--config", "auto", "--json", "--quiet", repo_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode in [0, 1]:
            sast_data = json.loads(result.stdout)
            with open(output_file, 'w') as f:
                json.dump(sast_data, f, indent=2)
            return sast_data
        else:
            print(f"Error SAST para {repo_name}: {result.stderr}")
            return {}
            
    except subprocess.TimeoutExpired:
        print(f"Timeout SAST para {repo_name}")
        return {}
    except Exception as e:
        print(f"Excepción SAST para {repo_name}: {e}")
        return {}