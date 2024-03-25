import sqlite3
from time import sleep

class ToDo:
    def __init__(self):
        self.db_execute('CREATE TABLE IF NOT EXISTS ToDo(nome text, status text)')
        self.main()
    

    def main(self): #Função principal do código
        while True:
            self.menu_principal('GERENCIADOR DE TAREFAS')
            op = str(input('\033[1mOpção =--> \033[m')).strip()
            if op == '1':
                self.new_task()
            elif op == '2':
                self.see_db()
            elif op == '3':
                self.manage_task()
            elif op == '4':
                self.sobre()
            elif op == '5':
                self.linha(33, 48)
                print('\033[1mMuito obrigado por usar o Gerenciador de tarefas!')
                sleep(1)
                print('Encerrando o programa', end='')
                for c in range(0,3):
                    print('.', end='', flush=True)
                    sleep(0.7)
                self.exit()
            else:
                self.error()

#Funções complementares
    def menu_principal(self, str, t=False): #Se o T for = False, ele não irá demonstrar as opções do menu principal
        self.str = f'{str}'
        l = len(self.str) #Recebendo a quantidade de caracteres do que eu vou escrever
        l2 = l*2 #Multiplicando por 2 para centralizar o título
        print('\033[32m-=\033[m'*(l+2))
        print(f"\033[1m {self.str:^{l2}}\033[m")
        print('\033[32m-=\033[m'*(l+2))
        print(self.opcoes_menuprincipal(n=True))
        print('\033[32m-=\033[m'*(l+2))
        

    def opcoes_menuprincipal(self, n=False): #Se n = True o texto virá com negrito
        if n:
            return f'''\033[1m1 - Registrar uma nova tarefa
2 - Ver todas as tarefas
3 - Gerenciar suas tarefas
4 - Sobre
5 - Sair do programa\033[m'''
        else:
            return f'''1 - Registrar uma nova tarefa
2 - Ver todas as tarefas
3 - Gerenciar suas tarefas
4 - Sobre
5 - Sair do programa'''
        

    def opcoes_manage_task(self, n=False): #Se n = True o texto virá com negrito
        if n:
            return '''\033[1m1 - Marcar as tarefas como concluído
2 - Excluir Tarefas
3 - Editar Tarefas
4 - Voltar para o Menu Principal\033[m'''
        else:
            return '''1 - Marcar as tarefas como concluído
2 - Excluir Tarefas
3 - Editar Tarefas
4 - Voltar para o Menu Principal'''
        

    def linha(self, cor=30, quantidade=1): #cor e quantidade de linhas que ele vai produzir
        print(f'\033[1;{cor}m-\033[m' * quantidade)

    
    def error(self): #Mensagem de erro
        print(f'\033[31mERRO: o que você digitou não é uma opção válida!\033[m')

    
    def back_toMenu(self, n=True): #Voltar para a main | if n = false vai ir direto para o menu principal
        if n:
            op = str(input('Aperte "Enter" para voltar para o menu principal: '))
            op = '2'
            if op == '2':
                print('Voltando para o \033[1;32mMenu Principal\33[m')
                sleep(1)
                print('\n\n\n\n')
                self.main()
        else:
            print('Voltando para o \033[1;32mMenu Principal\33[m')
            sleep(1)
            print('\n\n\n\n')
            self.main()
    

    def db_execute(self, query='', params=[]): #Executar tarefas no banco de dados
        with sqlite3.connect('banco_tarefas.db') as banco:
            cursor = banco.cursor()
            cursor.execute(query, params)
            banco.commit()


    def exit(self): #Sair do programa na hora
        print('\n\033[32m[PROGRAMA ENCERRADO COM SUCESSO]\033[m')
        exit()

#Funções principais
    def new_task(self): #Adicionando uma nova tarefa
        while True:
            self.linha(34, 48)
            new = str(input('Digite a tarefa a ser adicionada: ')).strip().capitalize()
            print('[1 - Para Confirmar]')
            print('[2 - Para Editar]')
            print('[3 - Para Cancelar / Sair]')
            self.linha(34, 48)
            con = str(input(f'Você confirma sua escolha: ')).strip()
            if con == '1':
                status = 'Incompleto'
                self.db_execute(f'INSERT INTO ToDo VALUES (?,?)',params=[new,status])
                sleep(0.5)
                print(f'\033[1;32mTarefa adicionada com sucesso!\033[m')
                sleep(1)
                print('[1 - Registrar uma nova tarefa]')
                print('[2 - Voltar para o Menu Principal]')
                op = str(input('\033[1mOpção =--> \033[m'))
                if op == '1':
                    self.new_task()
                else:
                    self.back_toMenu(n=False)
            elif con == '2':
                self.new_task()
            elif con == '3':
                self.main()
            else:
                self.error()


    def see_db(self, exit=True): #Ver todas as tarefas no banco de dados, exit=True quer dizer que ele vai voltar para o menu principal
        c=1
        banco = sqlite3.connect('banco_tarefas.db')
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM ToDo')
        lis = cursor.fetchall()
        if len(lis) == 0: #Caso não tenha nada no banco de dados, ele irá retornar essa mensagem
            self.linha(35,62)
            print(f'Você ainda não tem nenhuma tarefa cadastrada até o momento!')
            self.linha(35,62)
            sleep(1.5)
            self.back_toMenu(n=False)
        else: #Caso tenha, ele irá mostrar o que tem
            self.linha(35,62)
            print(f'Segue todas as tarefas que você tem cadastradas até o momento:')
            self.linha(35, 62)
            sleep(1)
            for n,s in lis:
                print(f'{c} - Nome: {n} | Status: {s}')
                sleep(0.5)
                c+=1
            self.linha(35, 48)
            if exit:
                self.back_toMenu()


    def manage_task(self): #Gerenciar as tarefas
        self.linha(36, 60)
        print(f'\033[1m{"GERENCIE AS SUAS TAREFAS AQUI":^60}\033[m')
        self.linha(36, 60)
        print(self.opcoes_manage_task(True))
        self.linha(36, 60)
        op = str(input('\033[1mOpção =--> \033[m')).strip()
        if op == '1': #Completar tarefas
            self.see_db(False)
            op = str(input('Digite o nome da tarefa da qual você deseja marcar como \033[1mconcluído\033[m: ')).strip().capitalize()
            try:
                banco = sqlite3.connect('banco_tarefas.db')
                cursor = banco.cursor()
                cursor.execute("SELECT * FROM ToDo WHERE nome = ?", (op,))  # Verificar se o que você escreveu está no banco de dados
                resultado = cursor.fetchone()
                
                if resultado: #Se a tarefa está no banco de dados
                    status_atual = resultado[1]  #Recebe o valor da segunda tabela da linha
                    if status_atual == 'Incompleto':
                        cursor.execute("UPDATE ToDo SET status = 'Completo' WHERE nome = ?", (op,))
                        banco.commit()
                        sleep(1)
                        print(f'\033[1;32mTAREFA {op} FOI MARCADA COMO CONCLUÍDA!\033[m')
                        sleep(1)
                        print('\033[1mVoltando para o Gerenciador de tarefas\033[m')
                        sleep(0.4)
                    else: #Se o resultado não for incompleto, ou seja, se estiver "Completo", ele não deixará mudar os status
                        print(f"\033[1;34mA tarefa '{op}' já está completa.\033[m")
                else: #Se a tarefa não existir
                    print(f"\033[1;34mA tarefa '{op}' não existe, nada foi feito.\033[m")
                banco.close()
            except sqlite3.Error as erro:
                print(f'\033[31mErro ao tentar mudar o status da tarefa: {erro}')
                print('Possíveis causas desse erro:')
                print('-Verifique como você digitou, provavelmente você digitou errado a tarefa desejada')
                print('-Tente novamente!')

            self.manage_task()

        elif op == '2': #Excluir tarefas
            self.see_db(False)
            all = str(input('\033[1;33mVocê deseja excluir todas as suas tarefas? [S/N] \033[m')).upper().strip() #Excluir todas as tarefas
            if all != 'S': #Se a "all" for diferente de sim, ele vai rodar qual tarefa ele deseja excluir
                op = str(input('Digite o nome da tarefa da qual você deseja \033[1mexcluir\033[m: ')).strip().capitalize()
                try:
                    banco = sqlite3.connect('banco_tarefas.db')
                    cursor = banco.cursor()
                    cursor.execute("SELECT * FROM ToDo WHERE nome = ?", (op,)) #Verificando se o que ele digitou está no banco de dados
                    resultado = cursor.fetchone()
                    if resultado:
                        cursor.execute("DELETE FROM ToDo WHERE nome = ?", (op,)) #Deletando a tarefa
                        banco.commit()
                        sleep(1)
                        print('\033[1;32mTAREFA REMOVIDA COM SUCESSO!\033[m')
                        sleep(1)
                        print('\033[1mVoltando para o Gerenciador de tarefas\033[m')
                        sleep(0.4)
                    else: #Caso digite errado
                        print(f"\033[1;34mA tarefa '{op}' não existe, nada foi excluído.\033[m")
                    banco.close()
                except sqlite3.Error as erro:
                    print(f'\033[31mErro ao tentar excluir a tarefa: {erro}')
                    print('Possíveis causas desse erro:')
                    print('-Verifique como você digitou, provavelmente você digitou errado a tarefa desejada')
                self.manage_task()
            else:
                confirm = str(input('\033[1;31mVocê tem certeza que deseja deletar todas as suas tarefas?\033[m \033[33m[S/N] \033[m')).upper().strip() #Uma outra confirmação se ele realmente quer deletar todas as suas tarefas
                if confirm != 'S': #Se for diferente de sim
                    print('\033[1mVoltando para o Gerenciador de tarefas\033[m')
                    sleep(0.4)
                    self.manage_task()
                else: #Deletando todas as tarefas do banco de dados
                    banco = sqlite3.connect('banco_tarefas.db')
                    cursor = banco.cursor()
                    cursor.execute("DELETE FROM ToDo")
                    banco.commit()
                    print('\033[1;32mTODAS AS TAREFAS FORAM REMOVIDAS COM SUCESSO!\033[m')
                    sleep(1)
                    self.back_toMenu(False)
    
        elif op == '3': #Editar tarefas
            self.see_db(False)
            op = str(input('Digite o nome da tarefa da qual você deseja \033[1meditar\033[m: ')).strip().capitalize()
            try:
                banco = sqlite3.connect('banco_tarefas.db')
                cursor = banco.cursor()
                cursor.execute("SELECT * FROM ToDo WHERE nome = ?", (op,)) #Verificar se o que você escreveu está no banco de dados
                resultado = cursor.fetchone()
                
                if resultado: #Se o resultado for True
                    new = str(input('Digite o nome da nova tarefa / edição da tarefa: ')).strip().capitalize()
                    cursor.execute("UPDATE ToDo SET nome = ? WHERE nome = ?", (new, op,)) #Trocando a tarefa
                    status_atual = resultado[1]  #Recebe o valor da segunda tabela da linha
                    if status_atual == 'Completo': #Se os status for "Completo", dar a opção de mudar para incompleto
                        self.linha(35,57)
                        opp = str(input('\n\n\033[1mDeseja mudar os status de Completo -> Incompleto? [S/N] \033[m')).strip().upper()
                        if opp != 'S':
                            print('Os status se manteve \033[1;32mCompleto\033[m')
                        else:
                            cursor.execute("UPDATE ToDo SET status = 'Incompleto' WHERE nome = ?", (new,)) #Colocando o status incompleto
                            print('Os status foi alterado de \033[1;32mCompleto\033[m -> \033[1mIncompleto\033[m')
                    banco.commit() 
                    sleep(1)
                    print(f'\033[1;32mTAREFA {op} FOI ATUALIZADA PARA {new}!\033[m')
                    sleep(1)
                    print('\033[1mVoltando para o Gerenciador de tarefas\033[m')
                    sleep(0.4)
                else:
                    print(f"\033[1;34mA tarefa '{op}' não existe, nada foi feito.\033[m")
                banco.close()
            except sqlite3.Error as erro:
                print(f'\033[31mErro ao tentar editar a tarefa: {erro}')
                print('Possíveis causas desse erro:')
                print('-Verifique como você digitou, provavelmente você digitou errado a tarefa desejada')
                print('-Tente novamente!')
            self.manage_task()

        elif op == '4': #Voltar para o menu
            self.back_toMenu(False)

        else: #Se escrever alguma informação errada
            self.error()
            self.manage_task()


    def sobre(self): #Sobre o projeto
        self.linha(36, 60)
        print(f'''\033[1mEste programa é um gerenciador de tarefas onde você pode:
1 - Criar tarefas;
2 - Ver todas as tarefas cadastradas até o momento;
3 - Gerenciar tarefas (Editar, Excluir e Concluir);

OBS: Este projeto é administrado por nomes, você gerencia todas as suas tarefas escrevendo o nome da tarefa
              
Programador e dono do projeto: Vinícius Flores Ribeiro
Versão: 1.9\033[m
''', end='')
        f'\n{self.linha(36, 60)}'
        self.back_toMenu()


#Programa Principal
programa = ToDo
programa()
