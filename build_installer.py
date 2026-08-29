import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
BUILD = ROOT / "build"


def main():
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name",
        "SistemaAutolavado",
        "--distpath",
        str(DIST),
        "--workpath",
        str(BUILD),
        "--specpath",
        str(ROOT),
        "app.py",
    ]

    print("Generando instalador...")
    print("Comando:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(ROOT))
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    exe = DIST / "SistemaAutolavado.exe"
    if exe.exists():
        print(f"Instalador generado: {exe}")
    else:
        print("Instalador generado en la carpeta dist/.")


if __name__ == "__main__":
    main()
