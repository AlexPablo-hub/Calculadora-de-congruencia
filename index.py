from math import gcd
from functools import reduce
import PySimpleGUI as sg
import tkinter as tk

def mdc_estendido(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = mdc_estendido(b % a, a)
        return g, y - (b // a) * x, x

def inverso_modular(a, m):
    g, x, _ = mdc_estendido(a, m)
    if g != 1:
        raise Exception('Inverso modular não existe')
    else:
        return x % m

def teorema_chines_do_resto(congruencias):
    M = reduce(lambda x, y: x * y[1], congruencias, 1)
    resultado = 0
    for ai, mi in congruencias:
        Mi = M // mi
        xi = inverso_modular(Mi, mi)
        resultado += ai * Mi * xi
    return resultado % M

def resolver_sistema_congruencias(congruencias):
    for i, (ai, mi) in enumerate(congruencias):
        for _, mj in congruencias[i + 1:]:
            if gcd(mi, mj) != 1:
                raise Exception('As congruências não são mutuamente primas')

    return teorema_chines_do_resto(congruencias)

def atualizar_listbox(listbox, congruencias):
    listbox.delete(0, tk.END)
    for ai, mi in congruencias:
        listbox.insert(tk.END, f'{ai} (mod {mi})')

# Função para criar a interface gráfica
def criar_interface():
    layout = [
        [sg.Text('Informe as congruências')],
        [sg.Text('Coeficiente linear:'), sg.InputText(key='a', size=(10, 1)), sg.Text(
            'Modulo:'), sg.InputText(key='m', size=(10, 1))],
        [sg.Text(''), sg.Listbox(values=[], select_mode=tk.SINGLE,
                                 size=(30, 5), key='congruencias_list', visible=False)],
        [sg.Button('Adicionar Congruência'), sg.Button(
            'Resolver'), sg.Button('Limpar')],
        [sg.Text(size=(30, 1), key='resultado')],
    ]

    window = sg.Window('Resolução de Sistema de Congruências', layout)

    congruencias = []
    listbox_elem = window['congruencias_list']

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Adicionar Congruência':
            try:
                a = int(values['a'])
                m = int(values['m'])
                congruencias.append((a, m))
                listbox_elem.update(visible=True)
                atualizar_listbox(listbox_elem.Widget, congruencias)
                window['a'].update('')
                window['m'].update('')
            except ValueError:
                sg.popup_error('Digite apenas números inteiros para a e m')
        elif event == 'Resolver':
            try:
                solucao = resolver_sistema_congruencias(congruencias)
                modulo = reduce(lambda x, y: x * y[1], congruencias, 1)
                window['resultado'].update(
                    f"A solução do sistema é x ≡ {solucao} (mod {modulo})")
            except Exception as e:
                sg.popup_error(str(e))
        elif event == 'Limpar':
            congruencias = []
            listbox_elem.update(visible=False)
            atualizar_listbox(listbox_elem.Widget, congruencias)
            window['resultado'].update('')
            window['a'].update('')
            window['m'].update('')

    window.close()

if __name__ == '__main__':
    criar_interface()
