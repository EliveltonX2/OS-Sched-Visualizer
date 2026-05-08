import PyInstaller.__main__
import os

# Nome do script principal
script_principal = "main.py"

# Nome do executável final
nome_exe = "Simulador_Escalonamento"

# Argumentos do PyInstaller
args = [
    script_principal,
    "--onefile",
    "--noconsole",
    f"--name={nome_exe}",
    "--collect-all=customtkinter",
    "--collect-all=matplotlib",
    "--clean",
]

if __name__ == "__main__":
    print(f"[*] Iniciando a criação do executável: {nome_exe}...")
    PyInstaller.__main__.run(args)
    print(f"\n[+] Concluído! O executável pode ser encontrado na pasta 'dist'.")
