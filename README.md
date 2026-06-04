# Skylert 🌤️

O **Skylert** é um sistema de monitoramento climático inteligente que permite aos usuários consultar a previsão do tempo em tempo real e configurar alertas automáticos por e-mail para condições climáticas extremas, como chuvas fortes, ventanias e temperaturas críticas.

---

## 🛠️ Tecnologias Utilizadas

- **Front-end:** HTML5, CSS3 (Glassmorphism), JavaScript (Vanilla)
- **Back-end:** Python, Flask
- **Banco de Dados e Autenticação:** Firebase (Firestore e Firebase Auth)
- **APIs Externas:** Open-Meteo API (Geocoding e Previsão do Tempo)
- **Background Worker:** Python + SMTP para envio automático de e-mails

---

## 🚀 Como rodar o projeto localmente

Como o projeto é dividido em **Front-end**, **API** e **Background Worker**, serão necessários **3 terminais abertos** para executar todos os serviços simultaneamente.

### 1. Pré-requisitos

Certifique-se de ter o **Python 3** instalado na máquina.

### Clonando o repositório

```bash
git clone https://github.com/SEU_USUARIO/skylert.git
cd skylert
```

---

### 2. Configurando o ambiente e instalando dependências

Crie um ambiente virtual e instale as dependências do projeto:

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual (Linux/macOS)
source venv/bin/activate

# Windows
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

---

### 3. Configurando as variáveis de ambiente

Por segurança, as credenciais não são armazenadas no repositório.

#### A) Arquivo `.env` (envio de e-mails)

Crie um arquivo chamado `.env` na raiz do projeto:

```env
EMAIL_REMETENTE=seu_email@gmail.com
EMAIL_SENHA_APP=sua_senha_gerada_no_google
```

> É necessário gerar uma **Senha de App** na sua conta Google para utilizar o SMTP do Gmail.

#### B) Arquivo `firebase-chave.json`

Baixe a chave privada da conta de serviço do Firebase:

**Firebase Console → Configurações do Projeto → Contas de Serviço → Gerar nova chave privada**

Salve o arquivo na raiz do projeto com o nome:

```text
firebase-chave.json
```

---

### 4. Iniciando a API (Back-end)

No primeiro terminal, com o ambiente virtual ativado:

```bash
python3 app.py
```

A API ficará disponível em:

```text
http://127.0.0.1:5000
```

---

### 5. Iniciando o Front-end

Abra um segundo terminal na pasta do projeto e execute:

```bash
python3 -m http.server 5500
```

Acesse:

```text
http://127.0.0.1:5500/index.html
```

> O Front-end detecta automaticamente quando está rodando localmente e direciona as requisições para a API Flask na porta 5000.

---

### 6. Iniciando o Background Worker (Alertas)

Abra um terceiro terminal, ative novamente o ambiente virtual e execute:

```bash
source venv/bin/activate

python3 alerta_climatico/main_worker.py
```

Esse serviço verifica periodicamente as condições climáticas e envia alertas por e-mail quando necessário.

---

## 📂 Estrutura Geral do Projeto

```text
skylert/
├── alerta_climatico/
│   └── main_worker.py
│   └── notification_worker.py
│   └── skylert_worker.py
├── app.py
├── dashboard.html
├── index.html
├── requirements.txt
├── firebase-chave.json
├── .env
└── ...
```

---

## ✨ Funcionalidades

- Consulta de previsão do tempo em tempo real
- Busca de cidades utilizando geocodificação
- Cadastro e autenticação de usuários
- Configuração personalizada de alertas climáticos
- Envio automático de notificações por e-mail
- Monitoramento contínuo através de Background Worker
