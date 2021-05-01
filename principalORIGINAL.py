"""
pip install PySide2
"""
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QMainWindow
from PySide2.QtCore import QFile
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtWidgets import*
from PySide2.QtGui import QImage
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtCore import QDate


import mysql.connector #Chamando biblioteca do banco de trabalho
import time # Biblioteca tempo
import os # Biblioteca do sistema Operacional
meu_db = ("iadenp",)

def conecta_db(db=None):#banco de dado recebe vazio
    if db == None:
        banco = mysql.connector.connect(
                    host = "localhost", #Local Hospedeiro
                    user = "root",
                    passwd = ""
                    )
        return banco
    else:
        banco = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database=db
                    )
        return banco
def existe_db():
    status = False
    try:
        db = conecta_db()
        cursor = db.cursor()
        cursor.execute("SHOW DATABASES")
        for banco in cursor:
            if banco==meu_db:
                status = True
        cursor.close()
        db.close()
    except BaseException as erro:
        print("Erro ao testar Banco: " + str(erro))
    return status
def criar_db():
    os.system("cls")
    try:
        db = conecta_db()
        cursor = db.cursor()

        cursor.execute("CREATE DATABASE " + meu_db[0])

        cursor.close()
        db.close()
        criar_tabela()

    except BaseException as erro:
        print("Erro na criação do Banco. ", str(erro))
def criar_tabela():
    try:
        db = conecta_db(meu_db[0])
        cursor = db.cursor()
        sql= "CREATE TABLE usuarios (id INT AUTO_INCREMENT PRIMARY KEY, usuario VARCHAR(20), passwd VARCHAR(10))"
        cursor.execute(sql)
        sql= "CREATE TABLE clientes (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), endereco VARCHAR(255),rg VARCHAR(13),cpf VARCHAR(14),contato VARCHAR(20),cargo VARCHAR(50),d_bat VARCHAR(30),d_con VARCHAR(30))"
        cursor.execute(sql)
        sql= "INSERT INTO usuarios (usuario, passwd) VALUES (%s, %s)"
        val= ("admin", "admin")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    except BaseException as erro:
        print("Erro ao criar tabelas " + str(erro))
def valida_usuario(us,pw):
    valida = False
    db = conecta_db(meu_db[0])
    cursor = db.cursor()

    sql = "SELECT * FROM usuarios WHERE usuario LIKE %s" #sql inserir
    val = (us,)

    cursor.execute(sql, val)

    usuarios = cursor.fetchone()

    if usuarios is not None and pw == usuarios[2]:
        valida = True
    else:
        valida = False
    return valida

#===============================================================================
def cpf_db(x):
    t=str(x)
    status = False
    db = conecta_db(meu_db[0])
    cursor = db.cursor()
    sql="SELECT * FROM clientes WHERE cpf=%s"
    val=(t,)
    cursor.execute(sql,val)
    resultado = cursor.fetchall()
    if resultado!=None:
        status = True
    else:
        status = False
    cursor.close()
    db.close()

    return status

def verificar_cpf(k):
    cpf=str(k)
    print("verificar_cpf: ",cpf)
    status= False
    b = ".-"
    for i in range(0,len(b)):
        cpf=cpf.replace(b[i],"")
    lcpf = [];
    for i in cpf:
        lcpf.append(i)
    m=10
    dv1=0
    dv2=0
    for i in range(9):
        dv1 += int(lcpf[i])*m
        m-=1
    dv1 = 11-(dv1%11)
    if dv1 > 9:
        dv1=0
    m=11
    for i in range(9):
        dv2 += int(lcpf[i])*m
        m-=1
    dv2 = 11-((dv2+(dv1*2))%11)
    if dv2 >9:
        dv2=0
    d1=cpf[9]
    d2=cpf[10]
    if int(dv1)==int(d1) and int(dv2)==int(d2):
        status=True
    return status
#===============================================================================
window = None

class cadastrar_usuario():
    janela = None
    def __init__(self,):
        global janela
        self.jan = QtGui.qApp
        self.arquivo = QFile("cadastro_de_usuario.ui")
        self.arquivo.open(QFile.ReadOnly)

        self.carrega = QUiLoader()
        janela = self.carrega.load(self.arquivo)

        janela.setFixedSize(438,606)
        def valida_cadastramento():

            us=janela.le_1.text()
            pw=janela.le_2.text()
            if valida_usuario(us,pw) ==True:
                us1=janela.le_3.text()
                pw1=janela.le_4.text()
                if len(us1)>=5 and len(us1)<=10 and len(pw1)>=5 and len(pw1)<=10:
                        try:
                            db = conecta_db(meu_db[0])
                            cursor = db.cursor()

                            sql= "UPDATE usuarios SET usuario = %s , passwd = %s WHERE usuarios.id= "+ str(1)
                            val=(us1, pw1)
                            cursor.execute(sql,val)

                            db.commit()

                            cursor.close()
                            db.close()

                            aviso("Cadastro de usuário", "Cadastro efetuado com sucesso.")
                            janela.close()
                        except BaseException as erro:
                            print("Erro ao crair Usuário", str(erro))
                else:
                    aviso("Cadastro de usuário", "Digite um novo usuário válido!")
            else:
                aviso("Cadastro de usuário", "Usuário admin inválido!")
        janela.btn_criar.clicked.connect(valida_cadastramento)
        self.arquivo.close()
        janela.show()
class c_membro():
    c_membro = None
    def __init__(self):
        global c_membro
        self.jan = QtGui.qApp
        self.arquivo = QFile("cadastro_de_membro.ui")
        self.arquivo.open(QFile.ReadOnly)

        self.carrega = QUiLoader()
        c_membro = self.carrega.load(self.arquivo)
        def cadastra_membro():
            nome= c_membro.le_nome.text()
            endereco= c_membro.le_endereco.text()
            d_bat= c_membro.le_d_bat.text()
            d_con= c_membro.le_d_con.text()
            contato= c_membro.le_contato.text()
            rg= c_membro.le_rg.text()
            cpf= c_membro.le_cpf.text()
            cargo = str(c_membro.combo_cargo.currentText())

            if nome!="" and endereco!="" and len(d_bat)==10 and len(d_con)==10 and len(contato)==16 and len(rg)==13 and len(cpf)==14:
                if cpf_db(cpf)==True:
                    if verificar_cpf(cpf)==True:
                            try:
                                db=conecta_db(meu_db[0])
                                cursor = db.cursor()

                                sql = "INSERT INTO clientes(nome, endereco, rg, cpf, contato, cargo, d_bat, d_con) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                                val =(str(nome), str(endereco), str(rg),str(cpf), str(contato), str(cargo), str(d_bat), str(d_con))
                                cursor.execute(sql, val)
                                db.commit()
                                aviso("Cadastro de Membro","Cadastro efetuado com sucesso...")
                                c_membro.le_nome.clear()
                                c_membro.le_endereco.clear()
                                c_membro.le_d_bat.setDate(QtCore.QDate(2000, 1, 1))
                                c_membro.le_d_con.setDate(QtCore.QDate(2000, 1, 1))
                                c_membro.le_contato.clear()
                                c_membro.le_rg.clear()
                                c_membro.le_cpf.clear()
                            except BaseException as erro:
                                    print("Erro no cadastrado do cliente.", str(erro))
                            finally:
                                    cursor.close()
                                    db.close()
                    else:
                        aviso("Cadastro de Membro","CPF Inválido, digite um cpf real")
                else:
                    aviso("Cadastro de Membro","CPF já cadastrado no banco")
            else:
                aviso("Cadastro de Membro","Por favor prencha todos os parâmetros")

        c_membro.btn_salvar.clicked.connect(lambda:cadastra_membro())#r

        self.arquivo.close()
        c_membro.show()
class pesquisa_exibir():
    pesquisa_exibir = None
    def __init__(self):
        global pesquisa_exibir
        self.jan = QtGui.qApp
        self.arquivo = QFile("exibircliente.ui")
        self.arquivo.open(QFile.ReadOnly)

        self.carrega = QUiLoader()
        pesquisa_exibir = self.carrega.load(self.arquivo)

        pesquisa_exibir.janela1.raise_()
        pesquisa_exibir.setFixedSize(287,91)

        def k():
            cp=pesquisa_exibir.le_cpf.text()
            if len(cp)==14:
                try:
                    db = conecta_db(meu_db[0])
                    cursor = db.cursor()

                    sql = "SELECT * FROM clientes WHERE cpf = %s"
                    val=(cp,)
                    cursor.execute(sql, val)

                    usuarios = cursor.fetchone()
                    if usuarios!=None:
                        pesquisa_exibir.janela2.raise_()
                        pesquisa_exibir.setFixedSize(661,581)
                        l=[]
                        for x in usuarios:
                             l.append(x)
                        print(l)
                        pesquisa_exibir.le_nome.setText(l[1])
                        pesquisa_exibir.le_endereco.setText(l[2])
                        pesquisa_exibir.le_rg.setText(l[3])
                        pesquisa_exibir.le_cpf_2.setText(l[4])
                        pesquisa_exibir.le_contato.setText(l[5])
                        pesquisa_exibir.le_cargo.setText(l[6])
                        pesquisa_exibir.le_d_bat.setText(l[7])
                        pesquisa_exibir.le_d_con.setText(l[8])
                    else:
                        aviso("CPF","CPF não cadastrado!!")
                except BaseException as e:
                    print("AVISO"," ERRO AO EXIBIR O MEMBRO"+str(e))
                finally:
                    cursor.close()
                    db.close()
        pesquisa_exibir.btn_ok.clicked.connect(k)
        self.arquivo.close()
        pesquisa_exibir.show()
class pesquisa_editar():
    pesquisa_editar = None
    def __init__(self):
        global pesquisa_editar
        self.jan = QtGui.qApp
        self.arquivo = QFile("editarcliente.ui")
        self.arquivo.open(QFile.ReadOnly)

        self.carrega = QUiLoader()
        pesquisa_editar = self.carrega.load(self.arquivo)

        pesquisa_editar.janela1.raise_()
        pesquisa_editar.setFixedSize(287,91)

        def k():
            cp=pesquisa_editar.le_cpf.text()
            if len(cp)==14:
                try:
                    db = conecta_db(meu_db[0])
                    cursor = db.cursor()

                    sql = "SELECT * FROM clientes WHERE cpf = %s"
                    val=(cp,)
                    cursor.execute(sql, val)

                    usuarios = cursor.fetchone()
                    if usuarios!=None:
                        pesquisa_editar.janela2.raise_()
                        pesquisa_editar.setFixedSize(661,581)
                        l=[]
                        for x in usuarios:
                             l.append(x)
                        c=["Auxiliar","Diácono","Presbítero","Pastor"]
                        for dado in c:
                            if dado==l[6]:
                                c.remove(dado)
                                c.insert(0, dado)

                        pesquisa_editar.combo_cargo_editar.addItem(c[0])
                        pesquisa_editar.combo_cargo_editar.addItem(c[1])
                        pesquisa_editar.combo_cargo_editar.addItem(c[2])
                        pesquisa_editar.combo_cargo_editar.addItem(c[3])
                        t=l[7]
                        if t[0]==0:
                            d1=f"{t[1]}"
                        else:
                            d1=f"{t[0]+t[1]}"
                        if t[3]==0:
                            d2=f"{t[4]}"
                        else:
                            d2=f"{t[3]+t[4]}"
                        d3=f"{t[6]}{t[7]}{t[8]}{t[9]}"
                        print(d3,d2,d1)
                        k=l[8]
                        if k[0]==0:
                            f1=f"{k[1]}"
                        else:
                            f1=f"{k[0]+k[1]}"
                        if k[3]==0:
                            f2=f"{k[4]}"
                        else:
                            f2=f"{k[3]+k[4]}"
                        f3=f"{k[6]}{k[7]}{k[8]}{k[9]}"
                        print(f3,f2,f1)

                        pesquisa_editar.le_nome.setText(l[1])
                        pesquisa_editar.le_endereco.setText(l[2])
                        pesquisa_editar.le_rg.setText(l[3])
                        pesquisa_editar.le_cpf_2.setText(l[4])
                        pesquisa_editar.le_contato.setText(l[5])
                        pesquisa_editar.le_d_bat.setDate(QtCore.QDate(int(d3), int(d2), int(d1)))
                        pesquisa_editar.le_d_con.setDate(QtCore.QDate(int(f3), int(f2), int(f1)))
                        def val_editar(l):
                            if cpf_db(cpf)==True:
                                if verificar_cpf(cpf)==True:
                                    print("posicao padrão",l[0])
                                    nome=pesquisa_editar.le_nome.text()
                                    endereco=pesquisa_editar.le_endereco.text()
                                    rg=pesquisa_editar.le_rg.text()
                                    cpf_2=pesquisa_editar.le_cpf_2.text()
                                    contato=pesquisa_editar.le_contato.text()
                                    cargo =str(c_membro.combo_cargo.currentText())
                                    d_bat=pesquisa_editar.le_d_bat.text()
                                    d_con=pesquisa_editar.le_d_con.text()
                                    c=[(l[0]),str(nome),str(endereco),str(rg),str(cpf_2),str(contato),str(cargo),str(d_bat),str(d_con)]
                                    variavel=["id","nome", "endereco", "RG","CPF", "Contato","Cargo", "d_bat", "d_con"]
                                    for x in range(8):
                                        print("posicao de x::",x)
                                        if l[x]!=c[x]:
                                            db = conecta_db(meu_db[0])
                                            cursor = db.cursor()
                                            print(f"variavel modificadas são: {variavel[x]}")
                                            sql= f"UPDATE clientes SET {variavel[x]} = %s WHERE clientes.id = " + str(l[0])
                                            val = (c[x],)
                                            cursor.execute(sql, val)
                                            db.commit()
                                            aviso("MEMBRO EDITAR","Membro editado com sucesso!!")
                                else:
                                    aviso("Editar Membro","CPF Inválido, digite um cpf real")
                            else:
                                aviso("Editar Membro","CPF já cadastrado no banco, escolha outro")
                        pesquisa_editar.btn_editar.clicked.connect(lambda:val_editar(l))
                    else:
                        aviso("CPF","CPF não cadastrado!!")
                except BaseException as e:
                    print("AVISO"," ERRO AO editar O MEMBRO"+str(e))
                finally:
                    cursor.close()
                    db.close()
        pesquisa_editar.btn_ok.clicked.connect(k)
        self.arquivo.close()
        pesquisa_editar.show()
class pesquisa_excluir():
    pesquisa_excluir = None
    def __init__(self):
        global pesquisa_excluir
        self.jan = QtGui.qApp
        self.arquivo = QFile("excluircliente.ui")
        self.arquivo.open(QFile.ReadOnly)

        self.carrega = QUiLoader()

        pesquisa_excluir=self.carrega.load(self.arquivo)

        pesquisa_excluir.janela1.raise_()
        pesquisa_excluir.setFixedSize(287,91)
        def x():
            cp=pesquisa_excluir.le_cpf.text()
            if len(cp)==14:
                try:
                    db = conecta_db(meu_db[0])
                    cursor = db.cursor()

                    sql = "SELECT * FROM clientes WHERE cpf = %s"
                    val=(cp,)
                    cursor.execute(sql, val)

                    usuarios = cursor.fetchone()
                    if usuarios!=None:
                        pesquisa_excluir.janela2.raise_()
                        pesquisa_excluir.setFixedSize(661,581)
                        l=[]
                        for x in usuarios:
                             l.append(x)
                        pesquisa_excluir.le_nome.setText(l[1])
                        pesquisa_excluir.le_endereco.setText(l[2])
                        pesquisa_excluir.le_rg.setText(l[3])
                        pesquisa_excluir.le_cpf_2.setText(l[4])
                        pesquisa_excluir.le_contato.setText(l[5])
                        pesquisa_excluir.le_cargo.setText(l[6])
                        pesquisa_excluir.le_d_bat.setText(l[7])
                        pesquisa_excluir.le_d_con.setText(l[8])
                        def y():
                            try:
                                db=conecta_db(meu_db[0])
                                cursor = db.cursor()
                                cpf =pesquisa_excluir.le_cpf.text()
                                print(cpf)
                                sql = "SELECT * FROM clientes WHERE cpf = %s"
                                val = (cpf,)
                                cursor.execute(sql, val)
                                resultado = cursor.fetchall()
                                if(len(resultado)>0):
                                    for r in resultado:
                                        sql= "DELETE FROM clientes WHERE clientes.id = "+ str(r[0])
                                        cursor.execute(sql)
                                        db.commit()
                                        aviso("CPF", "O MEMBRO "+cpf+" FOI EXCLUÍDO")
                                        pesquisa_excluir.close()
                            except BaseException as e:
                                print("AVISO"," ERRO AO EXCLUIR O MEMBRO"+str(e))
                            finally:
                                cursor.close()
                                db.close()
                        pesquisa_excluir.btn_excluir.clicked.connect(lambda:y())
                        cursor.close()
                        db.close()
                    else:
                        aviso("CPF","CPF não cadastrado!!")

                except BaseException as erro:
                    print("Erro ao pesquisa Cliente: "+str(erro))
            else:
                aviso("CPF","Digitos do cpf faltando")
        pesquisa_excluir.btn_ok.clicked.connect(x)

        self.arquivo.close()
        pesquisa_excluir.show()
class menu():
    menu = None
    def __init__(self,):
        global menu

        self.jan = QtGui.qApp
        self.arquivo = QFile("menu_principal.ui")
        self.arquivo.open(QFile.ReadOnly)

        self.carrega = QUiLoader()
        menu = self.carrega.load(self.arquivo)
        window.close()
        def tabela(t):
            if t=="ok":
                try:
                    db = conecta_db(meu_db[0])
                    cursor = db.cursor()
                    sql = "SELECT * FROM clientes"
                    cursor.execute(sql)

                    resultado = cursor.fetchall()

                    menu.tableWidget.setRowCount(0)
                    for row_number, row_data in enumerate(resultado):
                        menu.tableWidget.insertRow(row_number)

                        for colum_number, data in enumerate(row_data):
                            menu.tableWidget.setItem(row_number, colum_number-0.5, QtWidgets.QTableWidgetItem(data))
                except BaseException as erro:
                    print("Erro exibindo cliente.", str(erro))
                    input("Pressione [Enter] para continuar....")
                finally:
                    cursor.close()
                    db.close()
        tabela("ok")

        menu.btn_cadastra.clicked.connect(c_membro)
        menu.btn_editar.clicked.connect(pesquisa_editar)
        menu.btn_pesquisa.clicked.connect(pesquisa_exibir)
        menu.btn_excluir.clicked.connect(pesquisa_excluir)

        menu.btn_reload.clicked.connect(lambda:tabela("ok"))
        self.arquivo.close()
        menu.show()

def aviso(x,y):

    app = QtGui.qApp
    msg_box = QMessageBox()
    msg_box.setWindowTitle(x)
    msg_box.setText(y)
    msg_box.show()
    close = msg_box.exec()
if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file = QFile("login.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    if existe_db() == False:
        criar_db()
    def valida_usuario1():
        us=window.le_login.text()
        pw=window.le_senha.text()
        if valida_usuario(us,pw) == True:
            menu()
        else:
            aviso("Login","Login ou senha incorreto, tente novamente.")
            window.le_login.clear()
            window.le_senha.clear()

    window.btn_acessar.clicked.connect(valida_usuario1)

    window.btn_cadastrar.clicked.connect(cadastrar_usuario)

    ui_file.close()

    window.show()
    sys.exit(app.exec_())
