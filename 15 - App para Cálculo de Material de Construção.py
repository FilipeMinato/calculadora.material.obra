# Projeto - Calculadora de Tinta e Custo Total com Interface Gráfica
# Este programa permite ao usuário calcular:
# - A área útil de paredes a serem pintadas
# - A quantidade de tinta necessária (em litros)
# - O custo total usando latas de 20L e 3,6L
# O usuário pode inserir dados manualmente ou por área direta, incluindo aberturas como janelas ou portas.

import tkinter as tk
from tkinter import messagebox, simpledialog
import math

# ==============================
# Classe principal da aplicação
# ==============================
class CalculadoraTinta:
    def __init__(self, root):
        """
        Inicializa a interface gráfica principal.
        Define título, tamanho e os botões de ação.
        """
        self.root = root
        self.root.title("Cálculo de Tinta e Custo Total")
        self.root.geometry("600x400")
        self.area_total = 0.0  # Área acumulada de todas as paredes

        # Título amigável
        tk.Label(root, text="Bem-vindo ao Assistente de Pintura!",
                 font=("Helvetica", 16, "bold"), pady=20).pack()

        # Botão para iniciar cálculo
        tk.Button(root, text="Iniciar Novo Cálculo", command=self.calcular_tinta,
                  font=("Helvetica", 14), bg="#4CAF50", fg="white", width=25).pack(pady=10)

        # Botão para sair
        tk.Button(root, text="Encerrar Programa", command=self.root.quit,
                  font=("Helvetica", 14), bg="#f44336", fg="white", width=25).pack(pady=10)

    # ==========================
    # Funções auxiliares de entrada
    # ==========================
    def solicitar_float(self, mensagem):
        """
        Solicita um número decimal ao usuário.
        Aceita vírgula ou ponto como separador.
        """
        while True:
            entrada = simpledialog.askstring("Entrada", mensagem)
            if entrada is None:
                raise KeyboardInterrupt  # Permite cancelar toda a simulação
            entrada = entrada.replace(",", ".")
            try:
                return float(entrada)
            except ValueError:
                messagebox.showwarning("Entrada inválida", "Digite um número válido. Ex: 2.5 ou 2,5")

    def solicitar_int(self, mensagem):
        """
        Solicita um número inteiro ao usuário.
        """
        while True:
            entrada = simpledialog.askstring("Entrada", mensagem)
            if entrada is None:
                raise KeyboardInterrupt
            try:
                return int(entrada)
            except ValueError:
                messagebox.showwarning("Entrada inválida", "Digite um número inteiro válido.")

    def solicitar_opcao(self, mensagem, opcoes):
        """
        Solicita uma opção entre alternativas válidas.
        """
        while True:
            resposta = simpledialog.askstring("Escolha uma opção", mensagem)
            if resposta is None:
                raise KeyboardInterrupt
            resposta = resposta.strip().lower()
            if resposta in opcoes:
                return resposta
            messagebox.showwarning("Opção inválida", f"Escolha uma das opções: {', '.join(opcoes)}")

    # ==========================
    # Lógica principal do cálculo de tinta
    # ==========================
    def calcular_tinta(self):
        """
        Executa o fluxo completo:
        - Recebe áreas de paredes (com ou sem aberturas)
        - Calcula área total
        - Calcula litros de tinta necessários e custo
        - Sugere a melhor opção de compra
        """
        self.area_total = 0.0
        try:
            while True:
                # Usuário escolhe o tipo de entrada da parede
                tipo_parede = self.solicitar_opcao(
                    "Como deseja inserir a parede?\n(1) Altura e Comprimento\n(2) Área total em m²", ['1', '2'])

                # Cálculo da área da parede
                if tipo_parede == '1':
                    altura = self.solicitar_float("Digite a altura da parede (em metros):")
                    comprimento = self.solicitar_float("Digite o comprimento da parede (em metros):")
                    area_parede = altura * comprimento
                else:
                    area_parede = self.solicitar_float("Informe a área total da parede em m²:")

                # Verifica se há aberturas (portas/janelas)
                tem_abertura = self.solicitar_opcao("A parede possui aberturas (portas, janelas)? (s/n)", ['s', 'n'])

                area_abertura = 0.0
                if tem_abertura == 's':
                    tipo_abertura = self.solicitar_opcao(
                        "Como deseja informar a abertura?\n(1) Altura e Largura\n(2) Área total em m²", ['1', '2'])
                    if tipo_abertura == '1':
                        altura_abertura = self.solicitar_float("Altura da abertura (m):")
                        largura_abertura = self.solicitar_float("Largura da abertura (m):")
                        area_abertura = altura_abertura * largura_abertura
                    else:
                        area_abertura = self.solicitar_float("Informe a área total das aberturas em m²:")

                # Calcula área útil (sem abertura) e acumula
                area_util = max(0, area_parede - area_abertura)
                self.area_total += area_util
                messagebox.showinfo("Área Calculada", f"Área útil da parede adicionada: {area_util:.2f} m²")

                # Verifica se o usuário quer continuar
                mais = self.solicitar_opcao("Deseja inserir mais alguma área para pintura? (s/n)", ['s', 'n'])
                if mais != 's':
                    break

            # Solicita o número de demãos de tinta
            demãos = self.solicitar_int("Quantas demãos de tinta serão aplicadas?")
            rendimento = 6  # m² por litro de tinta
            litros_necessarios = (self.area_total * demãos) / rendimento

            # Preços fixos (poderiam vir de entrada do usuário)
            preco_lata_20l = 350
            preco_lata_3_6l = 89

            # Cálculo das latas
            latas_20l = int(litros_necessarios // 20)
            restante = litros_necessarios - (latas_20l * 20)
            latas_3_6l = math.ceil(restante / 3.6) if restante > 0 else 0
            custo_combinado = (latas_20l * preco_lata_20l) + (latas_3_6l * preco_lata_3_6l)

            # Resumo inicial
            resumo = f"Área total a ser pintada: {self.area_total:.2f} m²\n" \
                     f"Demãos: {demãos}\n" \
                     f"Litros de tinta necessários: {litros_necessarios:.2f} L\n"

            # Sugestão de economia
            if litros_necessarios <= 18:
                sobra = 20 - litros_necessarios
                custo_apenas_20l = preco_lata_20l
                custo_so_3_6l = math.ceil(litros_necessarios / 3.6) * preco_lata_3_6l

                if custo_apenas_20l < custo_so_3_6l:
                    resumo += f"\n⚠️ Vale mais a pena comprar 1 lata de 20L!\n" \
                              f"Sobrará: {sobra:.2f} L\n" \
                              f"Custo: R${custo_apenas_20l:.2f}\n" \
                              f"Custo com latas de 3,6L: R${custo_so_3_6l:.2f}\n" \
                              f"Economia: R${custo_so_3_6l - custo_apenas_20l:.2f}"
                else:
                    resumo += f"\n➡️ Mais econômico usar apenas latas de 3,6L.\n" \
                              f"Custo: R${custo_so_3_6l:.2f}"
            else:
                resumo += f"\nLatas de 20L: {latas_20l}\n" \
                          f"Latas de 3,6L: {latas_3_6l}\n" \
                          f"Valor total investido: R${custo_combinado:.2f}"

            messagebox.showinfo("Resultado Final", resumo)

        # Caso o usuário clique em "Cancelar" em qualquer entrada
        except KeyboardInterrupt:
            messagebox.showinfo("Simulação cancelada", "Você cancelou a simulação.\nVoltando para a tela inicial.")

# ==============================
# Execução da aplicação
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraTinta(root)
    root.mainloop()
