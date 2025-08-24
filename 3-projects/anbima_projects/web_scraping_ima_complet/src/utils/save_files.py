import os

def save_file_contents(complete_path, content):
    try:
        os.makedirs(os.path.dirname(complete_path), exist_ok=True)
        with open(complete_path, "wb") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error when saving {complete_path}: {e}")
        print(f"Erro ao salvar {complete_path}: {e}")