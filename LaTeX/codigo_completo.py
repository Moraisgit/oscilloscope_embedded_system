import T_Display
import math
import gc

#########################
#       VARIAVEIS       #
#########################
max_width = 240   # Largura do display
max_height = 135   # Altura do display
grid_height = max_height - 16   # Altura para desenhar a grelha
x_top_right_wifi = max_width - 16   # Coordenada x do icon Wifi
y_top_right_wifi = max_height - 16   # Coordenada y do icon Wifi
x_divisions = 10   # Numero de divisoes horizontais da grelha
y_divisions = 6   # Numero de divisoes verticais da grelha
x = []   # Vetor da escala horizontal
y = []   # Vetor da escala vertical
scales_time = [5, 10, 20, 50]   # Escalas horizontais no tempo
scales_volt = [1, 2, 5, 10]   # Escalas verticais de tensao
scales_spectrum_volt = [0.5, 1, 2.5, 5]   # Escalas verticais de tensao do espetro
scales_spectrum_freq = [240, 120, 60, 24]   # Escalas horizontais na frequencia
index_scales_vertical = 3   # Indice do vetor de escalas horizontais,, 20ms/div e 60Hz/div default
index_scales_horizontal = 2   # Indice do vetor de escalas verticais,, 10V/div default
voltages = []   # Lista de tensoes
factor = 1/29.3   # Fator do divisor resistivo
Vmax = 0   # Valor maximo de tensao
Vmin = 0   # Valor minimo de tensao
Vrms = 0   # Valor eficaz de tensao
Vavg = 0   # Valor medio de tensao
self = 0   # Argumento da funcao .send_mail
body = ""   # Corpo do email a enviar
spectrum = False   # Indica se estamos na representacao do espetro ou na normal
tft = T_Display.TFT()   # Instancia um objeto da classe TFT

####################### 
#       FUNCOES       #
#######################
'''
# Reset do display normal #
'''
def reset_display():
    tft.display_set(tft.BLACK, 0, 0, max_width, max_height)   # Apaga display
    tft.display_write_grid(0, 0, max_width, grid_height, x_divisions, y_divisions, True, tft.GREY1, tft.GREY2)   # Desenha grelha (c/ linhas centrais)
    tft.set_wifi_icon(x_top_right_wifi, y_top_right_wifi)   # Desenhar icon wifi

'''
# Desenhar o grafico normal #
'''
def draw_normal_plot():
    tft.display_nline(tft.YELLOW, x, y)   # Desenhar o sinal
    for i in x:   # Arranjar o grafico (apagar os pixeis que estao para la das margens do grafico)
        if y[i] >= grid_height:
            tft.display_pixel(tft.BLACK,x[i],y[i])
    tft.display_write_str(tft.Arial16, "%d V/div" % scales_volt[index_scales_vertical], 0, grid_height)   # Apresentar a escala vertical
    tft.display_write_str(tft.Arial16, "%d ms/div" % scales_time[index_scales_horizontal], 100, grid_height)   # Apresentar a escala horizontal

'''
# Ler valores ADC e calcular valores necessarios #
'''
def read_and_calculate():
    x_aux = []   # Coordenadas x
    y_aux = []   # Coordenadas y
    adc_points = []   # Lista de pontos de ADC
    voltages_aux = []   # Lista de tensoes
    Vmax_aux = 0   # Valor maximo de tensao
    Vmin_aux = 0   # Valor minimo de tensao
    Vavg_aux = 0   # Valor medio de tensao
    V = 0   # Conversao do valor do ADC para Volt

    adc_points = tft.read_adc(max_width, scales_time[index_scales_horizontal] * x_divisions)   # Le 240 pontos do ADC em [50, 100, 200, 500]ms
    voltages_aux = adc_points

    for n in range(max_width):
        # V = 0.00044028 * adc_points[n] + 0.091455   # Converte valor do ADC em Volt - Ajuste do Professor
        # V = V - 1   # Tensao entrada de referencia de 1V
        # V = V / factor   # Entra com o efeito do div. resistivo
        V = 0.012020968916394 * adc_points[n] - 24.238021692121710   # Converte valor do ADC em Volt - Ajuste experimental
        voltages_aux[n] = V

        pixel = grid_height/2 + (grid_height / (scales_volt[index_scales_vertical] * y_divisions))*V   # pix + [pix / (volt/div * div)]*volt = pix
        if pixel > grid_height:  # Quando o valor excede o espaco vertical superior simplesmente fica no limite superior do display
            pixel = grid_height
        x_aux.append(n)
        y_aux.append(round(pixel))
        
        if n == 0:   # Caso seja o primeiro ponto
            Vmax_aux = Vmin_aux = Vavg_aux = V
        else:
            Vavg_aux += V   # Ir somando para depois fazer o valor medio
            if V > Vmax_aux:   # Atualizar valor maximo de tensao
                Vmax_aux = V
            if V < Vmin_aux:   # Atualizar valor minimo de tensao
                Vmin_aux = V

    Vavg_aux /= max_width   # Calcular o valor medio dividinho pelo numero de amostras
    del adc_points, V, pixel   # Apagar variaveis ja nao necessarias

    return voltages_aux, Vmax_aux, Vmin_aux, Vavg_aux, x_aux, y_aux

'''
 # Reset do display para o botao 13 #
'''
def reset_button_13_display():
    tft.display_set(tft.BLACK, 0, 0, max_width, max_height)   # Apaga display
    tft.display_write_str(tft.Arial16, "Vmax = %.2f" % Vmax, 10, 60+20)   # Apresentar o valor Vmax
    tft.display_write_str(tft.Arial16, "Vmin = %.2f" % Vmin, 10, 40+20)   # Apresentar o valor Vmin
    tft.display_write_str(tft.Arial16, "Vavg = %.2f" % Vavg, 10, 20+20)   # Apresentar o valor Vavg
    tft.display_write_str(tft.Arial16, "Vrms = %.2f" % Vrms, 10, 20)   # Apresentar o valor Vrms
    tft.set_wifi_icon(x_top_right_wifi, y_top_right_wifi)   # Desenhar icon wifi

'''
# Calcular o valor eficaz #
'''
def calculate_rms_value():
    sum_squares = sum(value ** 2 for value in voltages)   # Soma dos quadrados
    Vrms_aux = (sum_squares / len(voltages)) ** 0.5   # Valor eficaz
    del sum_squares    # Apagar variaveis ja nao necessarias

    return Vrms_aux

'''
# Reset do display para o espetro #
'''
def reset_spectrum_display():
    tft.display_set(tft.BLACK, 0, 0, max_width, max_height)   # Apaga display
    tft.display_write_grid(0, 0, max_width, grid_height, x_divisions, y_divisions, False, tft.GREY1, tft.GREY2)   # Desenha grelha (s/ linhas centrais)
    tft.set_wifi_icon(x_top_right_wifi, y_top_right_wifi)   # Desenhar icon wifi

'''
# Desenhar o grafico do espetro #
'''
def draw_spectrum_plot():
    tft.display_nline(tft.MAGENTA, x, y)   # Desenhar o sinal
    for i in x:   # Arranjar o grafico (apagar os pixeis que estao para la das margens do grafico)
        if y[i] >= grid_height:
            tft.display_pixel(tft.BLACK,x[i],y[i])
    tft.display_write_str(tft.Arial16, "%.1f V/div" % scales_spectrum_volt[index_scales_vertical], 0, grid_height)   # Apresentar a escala vertical
    tft.display_write_str(tft.Arial16, "%d Hz/div" % scales_spectrum_freq[index_scales_horizontal], 100, grid_height)   # Apresentar a escala horizontal

'''
# Calcular a dft e espetro #
'''
def dft_and_spectrum(x_n):
    N = len(x_n)   # Numero de amostras
    x_aux = [n for n in range(0,max_width,1)]   # Vetor de frequencias
    y_aux = []   # Espetro de frequencia a devolver
    X_k = [0.0]*N   # DFT
    X_ss_k = [0.0]*N   # Espetro de frequencia

    for k in range(N//2):   # Ignorar o ponto N/2
        real = 0   # Parte real de X_k
        imag = 0   # Parte imaginaria de X_k
        for n in range(N - 1):   # Somatorio da equacao
            real += x_n[n] * math.cos(2 * math.pi * k * n / N)
            imag += x_n[n] * -math.sin(2 * math.pi * k * n / N)
        X_k[2*k] = math.sqrt(real**2 + imag**2)   # Modulo de X_k dois a dois pontos, porque queremos X_ss_k assim
        X_k[2*k + 1] = X_k[2*k]

        if k == 0:   # Expressao de X_ss_k
            X_ss_k[2*k] = X_k[2*k] / N
            X_ss_k[2*k + 1] = X_ss_k[2*k]
            pixel = X_ss_k[2*k] * (grid_height / (scales_spectrum_volt[index_scales_vertical] * y_divisions))   # pix + [pix / (volt/div * div)]*volt = pix
            if pixel > grid_height:  # Quando o valor excede o espaco vertical superior simplesmente fica no limite superior do display
                pixel = grid_height
            y_aux.append(round(pixel))
            pixel = X_ss_k[2*k + 1] * (grid_height / (scales_spectrum_volt[index_scales_vertical] * y_divisions))   # pix + [pix / (volt/div * div)]*volt = pix
            if pixel > grid_height:  # Quando o valor excede o espaco vertical superior simplesmente fica no limite superior do display
                pixel = grid_height
            y_aux.append(round(pixel))
        else:   # Expressao de X_ss_k
            X_ss_k[2*k] = 2*X_k[2*k] / N
            X_ss_k[2*k + 1] = X_ss_k[2*k]
            pixel = X_ss_k[2*k] * (grid_height / (scales_spectrum_volt[index_scales_vertical] * y_divisions))   # pix + [pix / (volt/div * div)]*volt = pix
            if pixel > grid_height:  # Quando o valor excede o espaco vertical superior simplesmente fica no limite superior do display
                pixel = grid_height
            y_aux.append(round(pixel))
            pixel = X_ss_k[2*k + 1] * (grid_height / (scales_spectrum_volt[index_scales_vertical] * y_divisions))   # pix + [pix / (volt/div * div)]*volt = pix
            if pixel > grid_height:  # Quando o valor excede o espaco vertical superior simplesmente fica no limite superior do display
                pixel = grid_height
            y_aux.append(round(pixel))
    
    del N, X_k, X_ss_k, real, imag, pixel    # Apagar variaveis ja nao necessarias

    return x_aux, y_aux

#########################################
#        PROGRAMA PRINCIPAL (main)      #
#########################################
reset_display()   # Reset do display normal 
voltages, Vmax, Vmin, Vavg, x, y = read_and_calculate()   # Ler valores ADC e calcular valores necessarios
draw_normal_plot()   # Desenhar o grafico normal

while tft.working():   # Ciclo principal do programa
    button = tft.readButton()   # Le estado dos botoes
    if button != tft.NOTHING:   # Quando algum botao for premido
        print("Button pressed:", button)
        if button == 11:   # Botao 1 click rapido (<1segundo)
            gc.collect()
            spectrum = False   # Ja nao estamos no espetro
            reset_display()   # Reset do display normal 
            index_scales_horizontal = 2   # Indice do vetor de escalas horizontais,, 20ms/div default
            index_scales_vertical = 3   # Indice do vetor de escalas verticais,, 10V/div default
            voltages, Vmax, Vmin, Vavg, x, y = read_and_calculate()   # Ler valores ADC e calcular valores necessarios
            draw_normal_plot()   # Desenhar o grafico normal
            gc.collect()

        if button == 12:   # Botao 1 click lento (>1segundo)
            gc.collect()
            Vrms = calculate_rms_value()   # Calcular o valor eficaz
            self = scales_time[index_scales_horizontal] * x_divisions   # Argumento da funcao .send_mail
            body = f"Tensao maxima (Vmax): {Vmax:.2f} V\nTensao minima (Vmin): {Vmin:.2f} V\nValor medio (Vav): {Vavg:.2f} V\nValor eficaz (Vrms): {Vrms:.2f} V"   # Corpo do email a enviar
            tft.send_mail(self/max_width, voltages, body, "antonio.v.morais.c@tecnico.ulisboa.pt")   # Enviar email da tabela com tempos e tensoes
            gc.collect()

        if button == 13:  # Botao 1 duplo click
            gc.collect()
            voltages, Vmax, Vmin, Vavg, x, y = read_and_calculate()   # Ler valores ADC e calcular valores necessarios
            Vrms = calculate_rms_value()   # Calcular o valor eficaz
            reset_button_13_display()   # Reset do display para o botao 1
            gc.collect()

        if button == 21:   # Botao 2 click rapido (<1segundo)
            gc.collect()
            index_scales_vertical += 1   # Incrementar o indice do vetor de escalas verticais
            if index_scales_vertical >= len(scales_volt):   # Indice do vetor de escalas verticais, caso seja o ultimo voltar ao inicio
                index_scales_vertical = 0
            if spectrum == True:   # Se estivermos no espetro
                reset_spectrum_display()   # Reset do display do espetro
                voltages, Vmax, Vmin, Vavg, x, y = read_and_calculate()   # Ler valores ADC e calcular valores necessarios
                x, y = dft_and_spectrum(voltages)   # Calcular o espetro
                draw_spectrum_plot()   # Desenhar o grafico do espetro
                gc.collect()
            else:
                reset_display()   # Reset do display normal
                voltages, Vmax, Vmin, Vavg, x, y = read_and_calculate()   # Ler valores ADC e calcular valores necessarios
                draw_normal_plot()   # Desenhar o grafico normal
                gc.collect()

        if button == 22:   # Botao 2 click lento (>1segundo)
            gc.collect()
            index_scales_horizontal += 1   # Incrementar o indice do vetor de escalas horizontais
            if index_scales_horizontal >= len(scales_time):   # Indice do vetor de escalas horizontais, caso seja o ultimo voltar ao inicio
                index_scales_horizontal = 0
            if spectrum == True:   # Se estivermos no espetro
                reset_spectrum_display()   # Reset do display do espetro
                voltages, Vmax, Vmin, Vavg, x, y = read_and_calculate()   # Ler valores ADC e calcular valores necessarios
                x, y = dft_and_spectrum(voltages)   # Calcular o espetro
                draw_spectrum_plot()   # Desenhar o grafico do espetro
                gc.collect()
            else:
                reset_display()   # Reset do display normal
                voltages, Vmax, Vmin, Vavg, x, y = read_and_calculate()   # Ler valores ADC e calcular valores necessarios
                draw_normal_plot()   # Desenhar o grafico normal
                gc.collect()

        if button == 23:   # Botao 2 duplo click
            gc.collect()
            spectrum = True   # Estamos no espetro
            reset_spectrum_display()   # Reset do display do espetro
            voltages, Vmax, Vmin, Vavg, x, y = read_and_calculate()   # Ler valores ADC e calcular valores necessarios
            x, y = dft_and_spectrum(voltages)   # Calcular o espetro
            draw_spectrum_plot()   # Desenhar o grafico do espetro
            gc.collect()