import tkinter as tk

janela = tk.Tk()
janela.title("Exemplo Tkinter")

botao = tk.Button(janela, text="Clique Aqui", command=ao_clicar)
botao.pack(pady=20)  # Adiciona o botão na janela com espaçamento vertical

janela.mainloop()
