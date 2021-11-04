import wx
import wx.grid as gridlib
import wx.richtext as rt
import json

class MainFrame(wx.Frame):
    def __init__(self, parent):
        style = wx.DEFAULT_FRAME_STYLE & (~wx.MAXIMIZE_BOX)
        super().__init__(parent, style=style)

        self.SetTitle('Simulador do consumo de energia elétrica')
        self.SetBackgroundColour(wx.RED)
        self.SetMinSize((984, 832))
        self.SetMaxSize((984, 2000))

        self._menu = wx.MenuBar()
        self._statusBar = self.CreateStatusBar()

        self._rowNumber = 44
        self._values = []
        self._tarifa = 0.55607408
        self._bandeira = 19.87
        self._debitoOutros = 2.98
        self._defaultData = []
        self._isOK = True

        self.__initUI()
        self.__getDataFromFile()

        self.__populateTable()
        for i in range(0, self._rowNumber):
            self.__onCellEdit(None, i)
        self.calculateTotalCost()

        self.Centre()

    def __initUI(self):
        ''' Inicializa a UI. '''

        master = wx.BoxSizer(wx.VERTICAL)

        self.__initMenu()

        self._grid = gridlib.Grid(self, size=(968, 600))
        self._rtc = rt.RichTextCtrl(self, -1, style=wx.TE_READONLY)

        self.__initGrid()
        self.__initRichText()

        master.Add(self._rtc, flag=wx.EXPAND, proportion=1)
        master.Add(self._grid, flag=wx.EXPAND, proportion=2)
        self.SetSizerAndFit(master)

    def __initMenu(self):
        ''' Inicializa o menu. '''

        # Menu 'Tabela'
        tabela = wx.Menu()
        reset = tabela.Append(-1, 'Resetar', 'Reseta a tabela com os dados de demonstração')
        add = tabela.Append(-1, 'Adicionar linha', 'Adiciona uma nova linha')

        self._menu.Append(tabela, 'Tabela')

        self.SetMenuBar(self._menu)

    def __initGrid(self):
        ''' Inicializa as propriedades do Grid. '''

        self._grid.CreateGrid(self._rowNumber, 7)
        self._grid.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.__onCellEdit)

        self._grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self._grid.SetColLabelValue(0, 'Outros Custos')
        self._grid.SetColSize(0, 160)
        self._grid.SetColLabelValue(1, 'Aparelho')
        self._grid.SetColSize(1, 200)
        self._grid.SetColLabelValue(2, 'Modelo')
        self._grid.SetColSize(2, 140)
        self._grid.SetColLabelValue(3, 'Potência')
        self._grid.SetColLabelValue(4, 'Quantidade')
        self._grid.SetColLabelValue(5, 'Tempo (horas por dia)')
        self._grid.SetColSize(5, 140)
        self._grid.SetColLabelValue(6, 'Custo (em reais)')
        self._grid.SetColSize(6, 120)

        self._grid.SetCellValue(0, 0, 'Tarifa')
        self._grid.SetCellBackgroundColour(0, 0, (255, 217, 102))
        self._grid.SetCellBackgroundColour(1, 0, (255, 242, 204))
        self._grid.SetReadOnly(0, 0)

        self._grid.SetCellValue(2, 0, 'Bandeira')
        self._grid.SetCellBackgroundColour(2, 0, (255, 217, 102))
        self._grid.SetCellBackgroundColour(3, 0, (255, 242, 204))
        self._grid.SetReadOnly(2, 0)

        self._grid.SetCellValue(4, 0, 'Débito de outros serviços')
        self._grid.SetCellBackgroundColour(4, 0, (255, 217, 102))
        self._grid.SetCellBackgroundColour(5, 0, (255, 242, 204))
        self._grid.SetReadOnly(4, 0)

        self._grid.SetCellValue(42, 5, 'Total eletrodomésticos')
        self._grid.SetCellBackgroundColour(42, 5, (146, 208, 80))
        self._grid.SetReadOnly(42, 5)

        self._grid.SetCellValue(43, 5, 'Total conta de luz')
        self._grid.SetCellBackgroundColour(43, 5, (0, 176, 80))
        self._grid.SetReadOnly(43, 5)

        for i in range(0, self._grid.GetNumberRows()):
            self._grid.SetReadOnly(i, 6)
            if i >= 6:
                self._grid.SetReadOnly(i, 0)

        self._grid.SetRowLabelSize(30)
        self._grid.DisableDragRowSize()
        self._grid.DisableDragColSize()
        # self._grid.InsertRows(40, 1)


    def __initRichText(self):
        ''' Inicializa a caixa de texto. '''

        self._rtc.WriteImage(wx.Bitmap('flyer.png'))
        self._rtc.GetCaret().Hide()

    def __getDataFromFile(self):
        ''' Popula a list self.data com os dados default to arquivo .json. '''

        with open(f"default_data.json", 'r', encoding='utf-8') as f:
            text = f.read()
            self._defaultData = json.loads(text)

    def __populateTable(self):
        ''' Reseta a tabela com os aparelhos para demonstração. '''

        for i in range(0, len(self._defaultData)):
            self._grid.SetCellValue(i, 1, self._defaultData[i]['device'])
            self._grid.SetCellBackgroundColour(i, 1, (214, 220, 229))
            self._grid.SetCellValue(i, 2, self._defaultData[i]['model'])
            self._grid.SetCellBackgroundColour(i, 2, (222, 235, 247))
            self._grid.SetCellValue(i, 3, self._defaultData[i]['power'])
            self._grid.SetCellBackgroundColour(i, 3, (255, 242, 204))
            self._grid.SetCellValue(i, 4, self._defaultData[i]['qtd'])
            self._grid.SetCellBackgroundColour(i, 4, (255, 242, 204))
            self._grid.SetCellValue(i, 5, self._defaultData[i]['time'])
            self._grid.SetCellBackgroundColour(i, 5, (255, 242, 204))

            self._grid.SetReadOnly(i, 1)
            self._grid.SetReadOnly(i, 2)

        for j in range(i + 1, i + 4):
            self._grid.SetCellBackgroundColour(j, 1, (214, 220, 229))
            self._grid.SetCellBackgroundColour(j, 2, (222, 235, 247))
            self._grid.SetCellBackgroundColour(j, 3, (255, 242, 204))
            self._grid.SetCellBackgroundColour(j, 4, (255, 242, 204))
            self._grid.SetCellBackgroundColour(j, 5, (255, 242, 204))
            self._grid.SetCellValue(j, 1, 'Outro')

        self._grid.SetCellValue(1, 0, str(self._tarifa))
        self._grid.SetCellValue(3, 0, str(self._bandeira))
        self._grid.SetCellValue(5, 0, str(self._debitoOutros))

    def __onCellEdit(self, event, index=None):
        ''' Chamanda quando cada célula é editada pelo usuário. '''

        if not event:
            row = index
        else:
            row = event.GetRow()
            col = event.GetCol()
            self.__replaceComma(row, col)
            if row in [1, 3, 5] and col == 0:   # Foi modificada a tarifa, bandeira ou outros débitos:
                self.__updateOtherVariables()
                self.__updateAllPrices()
                self.calculateTotalCost()
                return

        try:
            power = float(self._grid.GetCellValue(row, 3))
            qtd = float(self._grid.GetCellValue(row, 4))
            time = float(self._grid.GetCellValue(row, 5))
            self.__updateOneRowValue(row, power, qtd, time)

        except:
            self._grid.SetCellValue(row, 6, '0.00')

        # Durante a inicialização da tabela, essa função é chamada com event=None.
        # Só precisamos calcular quando o usuário muda alguma coisa.
        if event:
            self.calculateTotalCost()

    def __replaceComma(self, row, col):
        ''' Procura por uma ',' na string da célula. Se encontrar, substitui por '.'. '''

        value = self._grid.GetCellValue(row, col)
        self._grid.SetCellValue(row, col, value.replace(',', '.'))

    def __updateOneRowValue(self, row, power, qtd, time):
        ''' Atualiza o preço de apenas uma linha. `power`, `qtd` e `time` precisam já ser floats. '''

        if row in [12, 23, 25]:     # Verão (Freezer, Geladeira Simples, Geladeira Duplex)
            time -= 10
        elif row in [13, 24, 26]:   # Inverno (Freezer, Geladeira Simples, Geladeira Duplex)
            time -= 16

        cost = (power / 1000) * self._tarifa * time * qtd * 30
        self._grid.SetCellValue(row, 6, '{:.2f}'.format(cost))

    def __updateOtherVariables(self):
        ''' Atualiza as variáveis de tarifa, bandeira e outros débitos. Retorna True se todas estiverem OK,
        False caso contrário. '''

        try:
            self._tarifa = float(self._grid.GetCellValue(1, 0))
            self._bandeira = float(self._grid.GetCellValue(3, 0))
            self._debitoOutros = float(self._grid.GetCellValue(5, 0))
            return True
        except:
            self._grid.SetCellValue(42, 6, 'Error')
            self._grid.SetCellValue(43, 6, 'Error')
            return False

    def __updateAllPrices(self):
        ''' Atualiza os valores de todos os eletrodomésticos. Precisa ser chamada apenas quando a tarifa mudar. '''

        for i in range(0, self._rowNumber - 2):     # As duas últimas linhas são usadas para a exibição dos valores totais.
            try:
                power = float(self._grid.GetCellValue(i, 3))
                qtd = float(self._grid.GetCellValue(i, 4))
                time = float(self._grid.GetCellValue(i, 5))
                self.__updateOneRowValue(i, power, qtd, time)
            except:
                self._grid.SetCellValue(i, 6, '0.00')

    def calculateTotalCost(self):
        ''' Calcula o custo total e atualiza o valor nas duas últimas células da tabela. '''

        if not self.__updateOtherVariables():
            self._grid.SetCellValue(42, 6, 'Error')
            self._grid.SetCellValue(43, 6, 'Error')
            return

        totalSum = 0
        self._values.clear()
        for i in range(0, 42):
            value = float(self._grid.GetCellValue(i, 6))
            totalSum += value
            self._values.append(value)

        self._grid.SetCellValue(42, 6, '{:.2f}'.format(totalSum))  # Total Eletrodomésticos
        self._grid.SetCellValue(43, 6, '{:.2f}'.format(totalSum + self._bandeira + self._debitoOutros))  # Total Conta de Luz

        self.colorResultValues()

    def colorResultValues(self):
        ''' Colore as celulas de acordo com os valores exibidos. '''

        minV = min(self._values)
        maxV = max(self._values)

        for i in range(0, self._rowNumber - 2):
            value = float(self._grid.GetCellValue(i, 6))
            t = (value - minV) / (maxV - minV)
            if value == minV:
                t == 0
            elif value == maxV:
                t == 1

            self._grid.SetCellBackgroundColour(i, 6, (255, int(255 - 255 * t), int(255-255 * t)))

        self._grid.ForceRefresh()


app = wx.App()
frame = MainFrame(None)
frame.Show()
app.MainLoop()

# pyinstaller -F --clean --onefile --noconsole --hidden-import wx --hidden-import wx._xml C:\Users\Leandro\Desktop\Projects\SimuladorEnergetico\workspace\main.py