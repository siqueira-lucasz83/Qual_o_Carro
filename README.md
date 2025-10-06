# Qual é o Carro?

**Qual é o Carro?** é um jogo web interativo com visual retrô, onde o jogador tenta adivinhar o modelo de um carro com base em uma imagem pixelada e dicas progressivas. Além da jogabilidade, o sistema permite que o próprio jogador contribua com novos veículos, criando uma experiência dinâmica e colaborativa.

## Funcionalidades

- Jogo de adivinhação com dicas reveladas a cada tentativa incorreta  
- Sistema de pontuação baseado em desempenho e número de tentativas  
- Ranking global com destaque para os melhores jogadores  
- Cadastro e login com autenticação segura  
- Interface retrô pixelada inspirada em fliperamas dos anos 80  
- Modo administrador para gestão de veículos  
- Validação inteligente de carros com IA (modelo **Mistral**)  
- Possibilidade de **adicionar carros** ao jogo, aumentando a variedade e a interatividade  

## Tecnologias Utilizadas

- **Python + Flask**: backend e gerenciamento de rotas  
- **HTML + CSS**: estrutura visual com estilo retrô e responsivo  
- **JavaScript**: controle de tentativas, dicas e requisições assíncronas  
- **MySQL**: banco de dados relacional para jogadores e veículos  
- **Jinja2**: renderização dinâmica de páginas  
- **bcrypt**: criptografia de senhas  
- **dotenv**: gerenciamento de variáveis de ambiente  
- **Mistral (IA)**: validação de dados com linguagem natural  

## Estrutura do Projeto

- `app.py`: inicialização do Flask e conexão com o banco  
- `routes.py`: rotas do jogo, login, ranking e adição de carros  
- `Conexao.py`: funções de acesso ao banco de dados  
- `Jogadores.py`: cadastro, login e exibição de ranking  
- `Validar_carro.py`: validação com IA e registro de logs  
- Templates HTML e arquivos estáticos para a interface  

## Objetivo

Este projeto foi criado para unir entretenimento com aprendizado técnico, explorando:

- Desenvolvimento web com Flask  
- Integração com banco de dados relacional  
- Validação inteligente com IA  
- Design retrô e responsivo  
- Gamificação e ranking competitivo  
- Interatividade entre jogador e sistema por meio da **adição de novos carros**

## Contribuições

Este é um projeto pessoal, aberto para fins educacionais e demonstração de habilidades. Sugestões e melhorias são bem-vindas. Para contribuir, abra uma issue ou envie um pull request.

---

**Desenvolvido com dedicação por Lucas Siqueira.**

