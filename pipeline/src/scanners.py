import json
import subprocess
import os
from pathlib import Path


def generate_sbom(repo_path: str, output_dir: str) -> dict:
    """
    Genera un SBOM usando Syft para un repositorio dado.
    
    Args:
        repo_path: Ruta local del repositorio clonado
        output_dir: Directorio donde guardar el resultado JSON
        
    Returns:
        Dict con los datos del SBOM o dict vacío si falla
    """
    repo_name = Path(repo_path).name
    output_file = os.path.join(output_dir, f"sbom_{repo_name}.json")
    
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
            print(f"Error generando SBOM para {repo_name}: {result.stderr}")
            return {}
            
    except subprocess.TimeoutExpired:
        print(f"Timeout para {repo_name}")
        return {}
    except Exception as e:
        print(f"Excepción para {repo_name}: {e}")
        return {}