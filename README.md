# Skylert 🌤️

O **Skylert** é um sistema de monitoramento climático inteligente que permite aos usuários consultar a previsão do tempo em tempo real e configurar alertas automáticos (via e-mail) para condições climáticas extremas, como chuvas fortes, ventanias e temperaturas críticas.

## 🛠️ Tecnologias Utilizadas

* **Front-end:** HTML5, CSS3 (Glassmorphism), JavaScript (Vanilla)
* **Back-end:** Python, Flask
* **Banco de Dados & Autenticação:** Firebase (Firestore, Firebase Auth)
* **APIs Externas:** Open-Meteo API (Geocoding e Previsão do Tempo)
* **Background Worker:** Python puro com SMTP (para envio de e-mails automáticos)

---

## 🚀 Como rodar o projeto localmente

Como o projeto é dividido em Front-end, API e um script de Background Worker, você precisará de 3 terminais abertos para rodar tudo simultaneamente.

### 1. Pré-requisitos
Certifique-se de ter o [Python 3](https://www.python.org/) instalado na sua máquina.

# Faça o clone do repositório:
git clone https://github.com/SEU_USUARIO/skylert.git
cd skylert

### 2. Configurando o Ambiente e Dependências
Crie um ambiente virtual e instale as bibliotecas necessárias:

# Cria o ambiente virtual
python3 -m venv venv

# Ativa o ambiente virtual (Linux/macOS)
source venv/bin/activate
# No Windows use: venv\Scripts\activate

# Instala as dependências
pip install -r requirements.txt

### 3. Configurando as Variáveis de Ambiente (Credenciais)
# Por segurança, as credenciais não estão no repositório. Você precisará criar dois arquivos na raiz do projeto:

# A) Arquivo .env (Para envio de e-mails)
# Crie um arquivo chamado .env e coloque suas credenciais do Gmail (é necessário gerar uma "Senha de App" na sua conta do Google):

EMAIL_REMETENTE=seu_email@gmail.com
EMAIL_SENHA_APP=sua_senha_gerada_no_google

# B) Arquivo firebase-chave.json (Para acesso ao banco)
Baixe a chave privada da sua conta de serviço do Firebase (no painel do Firebase: Configurações do Projeto > Contas de Serviço > Gerar nova chave privada). Salve o arquivo na raiz do projeto com o nome exato de firebase-chave.json

### 4. Iniciando a API (Back-end)
# No seu primeiro terminal (com a venv ativada), inicie o servidor Flask:

python3 app.py
# A API ficará rodando em http://127.0.0.1:5000.

### 5. Iniciando o Front-end
# Abra um novo terminal na pasta do projeto e inicie um servidor estático para rodar o site:

python3 -m http.server 5500
Acesse no seu navegador: http://127.0.0.1:5500/index.html

(Nota: O Front-end está configurado para detectar se está rodando localmente e apontará automaticamente para a porta 5000 do Flask).

### 6. Iniciando o Background Worker (Alertas)
# Abra um terceiro terminal, ative a venv novamente, e rode o script responsável por verificar o clima e disparar os e-mails a cada 5 minutos:

source venv/bin/activate
python3 alerta_climatico/main_worker.py
