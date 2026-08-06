from pathlib import Path

def save_file_contents(complete_path: Path, content: bytes) -> bool:
    try:
        complete_path.parent.mkdir(parents=True, exist_ok=True)
        complete_path.write_bytes(content)
        return True
    except Exception as e:
        print(f"Error when saving {complete_path}: {e}")
        print(f"Erro ao salvar {complete_path}: {e}")
        return False
