# Sistema Transportadora

Um sistema completo de gerenciamento de transportadora com API REST em Python e interface web elegante.

## 📋 Descrição

Este projeto implementa um sistema completo para gerenciamento de uma transportadora, incluindo funcionalidades de autenticação, gerenciamento de remessas, veículos e clientes. O sistema oferece uma API REST robusta construída com FastAPI e uma interface web responsiva e moderna.

## ✨ Funcionalidades

### 🔐 Autenticação
- Sistema de login/logout seguro
- Controle de acesso baseado em tokens
- Contas de demonstração incluídas

### 📦 Gerenciamento de Remessas
- Criar novas remessas
- Rastrear status das remessas (Pendente, Em Trânsito, Entregue)
- Vincular remessas a clientes e veículos
- Visualizar histórico completo

### 🚛 Gerenciamento de Veículos
- Cadastro de veículos (placa, modelo, capacidade)
- Controle de status dos veículos
- Vinculação de veículos às remessas

### 👥 Gerenciamento de Clientes
- Cadastro completo de clientes
- Informações de contato atualizadas
- Vinculação de clientes às remessas

### 📊 Dashboard
- Estatísticas em tempo real
- Visão geral do sistema
- Métricas de performance

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

### Frontend
- **HTML5** - Estrutura da página
- **CSS3** - Estilização moderna e responsiva
- **JavaScript (ES6+)** - Interatividade e consumo da API

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior
- Navegador web moderno

### Passos para Instalação

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd sistemaTransportadora
   ```

2. **Instale as dependências do backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Execute o servidor:**
   ```bash
   python main.py
   ```

4. **Abra o navegador:**
   - Acesse: `http://localhost:8000` (API)
   - Abra `frontend/index.html` no navegador

## 📖 Como Usar

### Primeiro Acesso
1. Abra `frontend/index.html` no navegador
2. Use uma das contas de demonstração:
   - **Administrador:** `admin` / `admin123`
   - **Motorista:** `driver` / `driver123`

### Navegação
- **Painel:** Visão geral e estatísticas
- **Remessas:** Gerenciar encomendas
- **Veículos:** Controle da frota
- **Clientes:** Base de dados de clientes

### Criando uma Remessa
1. Acesse a seção "Remessas"
2. Preencha origem e destino
3. Selecione cliente e veículo (opcional)
4. Clique em "Criar Remessa"

## 📚 Documentação da API

### Autenticação
```
POST /login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

### Remessas
```
GET    /shipments          # Listar todas as remessas
POST   /shipments          # Criar nova remessa
GET    /shipments/{id}     # Obter remessa específica
PUT    /shipments/{id}     # Atualizar status da remessa
```

### Veículos
```
GET    /vehicles           # Listar todos os veículos
POST   /vehicles           # Criar novo veículo
PUT    /vehicles/{id}      # Atualizar veículo
DELETE /vehicles/{id}      # Excluir veículo
```

### Clientes
```
GET    /clients            # Listar todos os clientes
POST   /clients            # Criar novo cliente
PUT    /clients/{id}       # Atualizar cliente
DELETE /clients/{id}       # Excluir cliente
```

### Dashboard
```
GET /dashboard             # Estatísticas do sistema
```

## 📁 Estrutura do Projeto

```
sistemaTransportadora/
├── backend/
│   ├── main.py              # Servidor FastAPI principal
│   └── requirements.txt     # Dependências Python
├── frontend/
│   ├── index.html           # Interface principal
│   ├── styles.css           # Estilos CSS
│   └── script.js            # Lógica JavaScript
└── README.md                # Este arquivo
```

## 🔧 Desenvolvimento

### Executando em Modo de Desenvolvimento

1. **Backend:**
   ```bash
   cd backend
   python main.py
   ```

2. **Frontend:**
   - Abra `frontend/index.html` em um navegador
   - As mudanças em HTML/CSS/JS são refletidas automaticamente

### Adicionando Novos Recursos

1. **Backend:** Adicione novos endpoints em `backend/main.py`
2. **Frontend:** Atualize `frontend/script.js` para consumir novos endpoints
3. **UI:** Modifique `frontend/index.html` e `frontend/styles.css`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte ou dúvidas, entre em contato através das issues do GitHub.

## 🔄 Atualizações Futuras

- [ ] Sistema de notificações
- [ ] Relatórios avançados
- [ ] Integração com mapas
- [ ] Aplicativo móvel
- [ ] Multi-idioma
- [ ] Backup automático

---

**Desenvolvido com ❤️ para demonstrar habilidades em desenvolvimento full-stack**