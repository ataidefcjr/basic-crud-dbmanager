import os
from pyshortcuts import make_shortcut

def create_desktop_shortcut():
    # Diretório onde o script create_shortcut.py está localizado
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Caminho para o arquivo main.py
    main_file = os.path.join(current_dir, 'main.py')

    #Vefifica se é windows
    is_windows = sys.platform.startswith('win')
    if is_windows:
        executable = 'pythonw'
    else:
        executable = 'python3'

    # Criar atalho na área de trabalho
    make_shortcut(main_file, name='Gerenciador de Vendas', description='Banco de Dados', terminal=False, executable=executable, working_dir=current_dir)

    print('''--------------------------------------------------------------------------------------
    \n ----------------------------- Shortchut added to desktop ----------------------------
    \n--------------------------------------------------------------------------------------
    \n ************************ If doesn't work, run python main.py ************************''')

if __name__ == '__main__':
    create_desktop_shortcut()
