import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Mario123@1",
  database="base99"
)

def atualizarSizeDocumento(id,size=15):
    baseCursor = db.cursor(buffered=True)
    baseSql = 'update documentos set Size={0} where Id={1}'.format(size,id)
    baseCursor.execute(baseSql)
    db.commit()
    return baseCursor.rowcount

def selecionarDisciplinas():
    baseCursor = db.cursor(buffered=True)
    baseSql = 'select * from disciplinas'
    baseCursor.execute(baseSql)
    return baseCursor.fetchall()

def selecionarDisciplina(id):
    baseCursor = db.cursor(buffered=True)
    baseSql = 'select id_doc from disciplinas where Id={0}'.format(id)
    baseCursor.execute(baseSql)
    return baseCursor.rowcount

def atualizarDisciplina(id):
    baseCursor = db.cursor(buffered=True)
    baseSql = 'update disciplinas set Status=1 where Id={0}'.format(id)
    baseCursor.execute(baseSql)
    db.commit()
    return baseCursor.rowcount

def quantidadeDeDocumentos():
    baseCursor = db.cursor(buffered=True)
    baseSql = 'select * from documentos where Status=0'
    baseCursor.execute(baseSql)
    return baseCursor.rowcount

def inserirDisciplina(informacao):
    baseCursor = db.cursor(buffered=True)

    baseSql = 'insert into disciplinas (Id,' \
              'Name,' \
              'Alias,' \
              'Status,'\
              'Score' \
              ') values ({0},' \
              '"{1}",' \
              '"{2}",' \
              '0,'\
              '{3})'.format(
        informacao[0],
        informacao[1],
        informacao[2],
        informacao[3]
    )


    baseCursor.execute(baseSql)
    db.commit()
    return  baseCursor.rowcount

def selecionarDocumentos():
    baseCursor = db.cursor(buffered=True)
    baseSql = 'select * from documentos where Status=0 and Size=0'
    baseCursor.execute(baseSql)
    return baseCursor.fetchall()

def atualizarDocumento(id):
    baseCursor = db.cursor(buffered=True)
    baseSql = 'update documentos set Status=1 where Id={0}'.format(id)
    baseCursor.execute(baseSql)
    db.commit()
    return baseCursor.rowcount

def inserirDocumento(informacoes):

    baseCursor = db.cursor(buffered=True)

    for informacao in informacoes:

        tags = ''
        for q in informacao[16]:
            tags=tags+str(q[1]).replace('|','')+'| '

        baseSql = 'insert into documentos (' \
                  'Id, ' \
                  'Name, ' \
                  'Type, ' \
                  'Extension, ' \
                  'FileUrl, ' \
                  'Author_Id, ' \
                  'Author_Name, ' \
                  'Author_ImageUrl, ' \
                  'Author_UniversityShortName, ' \
                  'FilePreview_Id, ' \
                  'FilePreview_FileId, ' \
                  'FilePreview_FolderUrl, ' \
                  'FilePreview_PageCount, ' \
                  'Subject_Id, ' \
                  'Subject_Name, ' \
                  'Subject_Alias, ' \
                  'Tags, ' \
                  'Content, ' \
                  'Status, ' \
                  'Downloads, ' \
                  'Views, '\
                  'size) values (' \
                  '{0},' \
                  '"{1}",' \
                  '{2},' \
                  '"{3}",' \
                  '"{4}",' \
                  '{5},' \
                  '"{6}",' \
                  '"{7}",' \
                  '"{8}",' \
                  '{9},' \
                  '{10},' \
                  '"{11}",' \
                  '{12},' \
                  '{13},' \
                  '"{14}",' \
                  '"{15}",' \
                  '"{16}",' \
                  '"{17}",' \
                  '{18},' \
                  '{19},' \
                  '{20})'.format(
                    informacao[0],
                    str(informacao[1]).replace('"','\''),
                    informacao[2],
                    str(informacao[3]).replace('"','\''),
                    str(informacao[4]).replace('"','\''),
                    informacao[5],
                    str(informacao[6]).replace('"','\''),
                    str(informacao[7]).replace('"','\''),
                    str(informacao[8]).replace('"','\''),
                    informacao[9],
                    informacao[10],
                    str(informacao[11]).replace('"','\''),
                    informacao[12],
                    informacao[13],
                    str(informacao[14]).replace('"','\''),
                    str(informacao[15]).replace('"','\''),
                    str(tags).replace('"','\''),
                    'null'.replace('"','\''),
                    0,
                    0,
                    0,
                    0
        )

        baseCursor.execute(baseSql)
        db.commit()
        return baseCursor.rowcount


def selecionarDocumento(id):
    baseCursor = db.cursor(buffered=True)
    baseSql = 'select id_doc from documentos where Id={0}'.format(id)
    baseCursor.execute(baseSql)
    return baseCursor.rowcount
