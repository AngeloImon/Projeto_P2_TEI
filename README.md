> 📘 This README is available in: [🇺🇸 English](README.en.md) | [🇧🇷 Português](README.md)

# 📘 Projeto de Tópicos Especiais em Informática — Aplicativo de Organização de Estudos

Aplicativo web desenvolvido em Python com a biblioteca **NiceGUI**, voltado para auxiliar usuários na organização dos seus estudos por meio de criação de planos, gerenciamento de cronogramas semanais e exportação de dados. O sistema é intuitivo, responsivo e com múltiplas funcionalidades integradas.

---

## 🎯 Objetivo

- Criar uma interface acessível para cadastro e login de usuários.
- Permitir o planejamento de estudos com base em calendário e dias da semana.
- Organizar múltiplos planos de estudo de forma visual e interativa.
- Importar e exportar dados dos planos registrados.
- Exibir um dashboard com visão geral dos planos cadastrados e métricas de uso.

---

## 🧱 Estrutura do Projeto

O projeto é modularizado, com componentes organizados na pasta `Telas`, e utiliza um sistema de rotas para navegação entre páginas.

### Principais Módulos:

- `main.py` — Arquivo principal que inicializa a interface e as rotas.
- `login.py` / `signup.py` — Telas de autenticação.
- `dashboard.py` — Visão geral dos planos ativos.
- `meus_planos.py` — Página com lista dos planos do usuário.
- `novo_plano.py` — Formulário para criação de novos planos.
- `novo_plano_dias_semana.py` — Configuração de planos com foco em dias da semana.
- `novo_plano_calendario.py` — Planejamento baseado em datas específicas.
- `sobre.py` — Página institucional com informações do app.
- `importar_exportar_dados_geral.py` — Exportação/importação completa.
- `importar_exportar_dados_individual.py` — Gerenciamento de dados por plano.

Outros arquivos incluem funções auxiliares e integração com Firebase via `firebase_firestore.py`.

---

## 💻 Tecnologias Utilizadas

- 🐍 **Python**
- 🌐 **NiceGUI** (interface web declarativa)
- 🧪 **dotenv** (gestão de variáveis de ambiente)
- ☁️ **Firebase Firestore** (armazenamento de dados)
- 📦 Estrutura modular com rotas e carregamento dinâmico de páginas

---

## 🧠 Funcionalidades

- Autenticação via páginas de login e cadastro
- Criação de planos de estudo com múltiplas configurações:
  - Por calendário
  - Por dias da semana
- Visualização organizada com cards e botões estilizados
- Exportação de dados em formato estruturado
- Interface responsiva e intuitiva com animações e gradientes
- Cabeçalho padronizado em todas as páginas com links fixos

---

## 📱 Visual da Página Inicial

- Header com título e links rápidos
- Card central com apresentação do sistema
- Botões para login e cadastro
- Texto explicativo com Markdown
