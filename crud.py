#coding: utf-8

#sudo apt-get install python-pip -- instalar python
#sudo apt-get install python-tk -- instalar o TK
#sudo pip install appjar -- intalar a bib. appJar (Grafica)
#sudo apt-get install python-mysqldb -- Conexão python e mySQL

from appJar import gui #importa a bib
import MySQLdb



##conexao = MySQLdb.connect("192.168.56.101", "aluno", "aluno2017", "mundo")
#Nome conexão com BD = conectando ao BD ( IP Servidor, usuario, senha, nomeBD)

#conexao.select_db("mundo") -- Outra maneira de selecionar o BD
##cursor = conexao.cursor()

#cursor.execute("SELECT * FROM Pais;")
#result1 = cursor.fetchone() -- Pegar o primeiro resultado
#result = cursor.fetchall() -- pega tds os resultados restantes

def login(btn):
    if btn == "Cancelar":
        app.stop()

    global conexao

    global cursor

    host = app.getEntry("Host")   
    user = app.getEntry("Usuario") 
    senha = app.getEntry("Senha") 
    

    if user == "aluno" and host == "192.168.56.101":
    	if senha == "aluno2017":
    		app.infoBox("Sucesso", "Você está logado!")
    		conexao = MySQLdb.connect(host, user, senha, "mundo")
    		cursor = conexao.cursor()
			
    		app.showSubWindow('CRUD_DE_MYSQL')

    	else:
    		app.errorBox("Falha login", "Senha invalida")
    else:
    	app.errorBox("Falha login", "Usuario ou host invalido")
     

# create a GUI variable called app
app = gui("Login Window", "400x200")

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Tela de login")
app.setLabelBg("title", "blue")
app.setLabelFg("title", "orange")

app.addLabelEntry("Host")
app.addLabelEntry("Usuario")
app.addLabelSecretEntry("Senha")

# link the buttons to the function called press
app.addButtons(["Logar", "Cancelar"], login)

app.setFocus("Usuario")


def usando(btn): # -- Função do botão
	# print "Exemplo" -- Exibir texto via terminal
	app.infoBox("Mensagem de aviso!", "Você me usou Vou lhe usar!") # -- Exibe em uma janela nova
	pass

def pesquisar(btn):
	#app.textBox("Digite", "Digite seu nome: ") # -- Caixa de texto para entrar com algum texto.
	termo = app.getEntry("txtBusca")
	if termo == '':
		app.errorBox("Erro",'Informe um termo para pesquisar!')
	else:
		# SELECT * FROM Cidade WHERE NomeCidade LIKE '%Belo%'
		cursor.execute("SELECT Cidade.NomeCidade, Estado.NomeEstado FROM Cidade "+
						"INNER JOIN Estado ON Estado.idEstado = Cidade.Estado_idEstado "
						+ "WHERE NomeCidade LIKE '%" + termo + "%'")

		rs = cursor.fetchall()

		app.clearListBox("lBusca")

		for x in rs:
			app.addListItem("lBusca", x[0] + ' - ' + x[1])
			#app.addListItems ("lBusca", rs)

def exibir(btn):

	cursor.execute("SELECT Pais.nomePais, Estado.nomeEstado, Cidade.nomeCidade FROM mundo.Pais INNER JOIN mundo.Estado ON Estado.Pais_idPais = Pais.idPais INNER JOIN mundo.Cidade ON Cidade.Estado_idEstado = Estado.idEstado")
	rs = cursor.fetchall()

	app.clearListBox("lBusca")

	for x in rs:
		app.addListItem("lBusca", x[0] + ' - ' + x[1] + ' - ' + x[2])



def inserir(btn):
	app.showSubWindow('janela_inserir')

def salvar_estado(btn):
	cidade = app.getEntry('txtcidade')
	idestado = app.getEntry('txtestado')
	cursor.execute("INSERT INTO Cidade (NomeCidade, Estado_idEstado) VALUES('{}',{})".format(cidade,idestado))
	#cursor.execute("INSERT INTO Cidade (NomeCidade, Estado_idEstado) VALUES('%s',%s)" % (cidade,idestado))
	conexao.commit()
	app.hideSubWindow('janela_inserir')
	app.infoBox("Salvo", "Salvo com suecesso!")

def excluir(btn):
	app.showSubWindow('janela_excluir')

def excluir_estado(btn):
	eCidade = app.getEntry('txtNcidade')
	cursor.execute("DELETE FROM Cidade WHERE nomeCidade = ('{}')".format(eCidade))
	conexao.commit()
	app.hideSubWindow('janela_excluir')
	app.infoBox("Excluido", "Excluido com suecesso!")

def atualizar(btn):
	app.showSubWindow('janela_atualizar')


def atualizar_estado(btn):
	cidadeVelha = app.getEntry('txtCidadeVelha')
	cidadeNova = app.getEntry('txtCidadeNova')
	cursor.execute("UPDATE Cidade SET nomeCidade = ('{}') WHERE nomeCidade = ('{}')".format(cidadeNova,cidadeVelha))
	conexao.commit()
	app.hideSubWindow('janela_atualizar')
	app.infoBox("Alterado", "Alterado com suecesso!")

def teste(btn):
	app.showSubWindow('CRUD_DE_MYSQL')

#app = gui("CRUD de MySQL", "600x300") # -- Titulo, tamanho da janela



# this is a pop-up -- INSERIR
app.startSubWindow("janela_inserir", modal=True)
app.addLabel("l1", "Inserindo dados...")
app.addEntry('txtestado')
app.addEntry('txtcidade')
app.addButton('Salvar cidade',salvar_estado)
app.setEntryDefault("txtestado", "ID do Estado")
app.setEntryDefault("txtcidade", "Nome da cidade")
app.stopSubWindow()

# this is a pop-up -- EXCLUIR
app.startSubWindow("janela_excluir", modal=True)
app.addLabel("l2", "Excluindo dados...")
app.addEntry('txtNcidade')
app.addButton('Excluir cidade',excluir_estado)
app.setEntryDefault("txtNcidade", "Nome da cidade")
app.stopSubWindow()

# this is a pop-up -- ATUALIZAR
app.startSubWindow("janela_atualizar", modal=True)
app.addLabel("l3", "Atualizando dados...")
app.addEntry('txtCidadeVelha')
app.addEntry('txtCidadeNova')
app.addButton('Alterar cidade',atualizar_estado)
app.setEntryDefault("txtCidadeVelha", "Cidade para alterar")
app.setEntryDefault("txtCidadeNova", "Nome da cidade novo")
app.stopSubWindow()

# -- Adiciona os botões: Texto, Função, Pos. Linha, Pos. Coluna)
app.startSubWindow("CRUD_DE_MYSQL", modal=True)
app.setGeometry("600x300")
app.addButton("Exibir dados", exibir, 1,0)
app.addButton("Inserir dados", inserir, 1,1)
app.addButton("Atualizar dados", atualizar, 2,0)
app.addButton("Excluir dados", excluir, 2,1)
app.addEntry("txtBusca",3,0,2)
app.setEntryDefault("txtBusca", "Digite o termo...")
app.addButton("Pesquisar", pesquisar, 4,0,2)
app.addListBox("lBusca", [], 5,0,2)
app.setListBoxRows("lBusca",5)
app.stopSubWindow()


#x = app.textBox("Nome", "Informe seu nome")
#app.setLabel("lNome", "Bem-Vindo " + x)
app.go() # -- executa a exibição da janela


#app.setBg("orange")
#app.setGeometry("400x400")
#app.setTransparency(25)
#app.setStopFunction(checkDone)
#app.addLabel("l1", "In sub window")
#app.stopSubWindow()