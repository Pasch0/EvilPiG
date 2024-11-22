import streamlit as st
import subprocess

# Título do aplicativo
st.title("Shell Interativo")

# Campo de entrada para o usuário digitar comandos
command = st.text_input("Digite um comando:", "")

if st.button("Executar"):
    if command:
        try:
            # Executa o comando e captura a saída
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            st.text_area("Output:", output.decode('utf-8'), height=300)
        except subprocess.CalledProcessError as e:
            st.error(f"Erro ao executar o comando: {e.output.decode('utf-8')}")
    else:
        st.warning("Por favor, insira um comando.")