# Fundamentos de segurança da informação

Base de conhecimento usada pelas skills `vulnerability-analysis` e `security-study-path`. Leia este arquivo sempre que a conversa envolver segurança.

## Conceitos essenciais

| Conceito | Definição simples | Exemplo |
|----------|-------------------|---------|
| Ativo | Tudo que tem valor e precisa ser protegido | banco de dados de clientes, servidor, código-fonte |
| Vulnerabilidade | Uma fraqueza que pode ser explorada | login que monta SQL juntando o texto digitado |
| Ameaça | Quem ou o que pode explorar a fraqueza | um atacante na internet, um bot automatizado |
| Exploração | O ato de usar a vulnerabilidade | digitar `' OR '1'='1` no campo de usuário |
| Risco | A chance de a ameaça explorar a vulnerabilidade, combinada com o estrago que isso causa | vazamento da base de clientes |
| Controle | Medida que reduz o risco | consulta parametrizada, firewall, MFA |

Analogia: a vulnerabilidade é a janela aberta, a ameaça é o ladrão no bairro e o risco é a chance de ele entrar multiplicada pelo valor do que está dentro da casa.

## Tríade CID

| Pilar | Pergunta-chave | Falha típica |
|-------|----------------|--------------|
| Confidencialidade | Só quem deve ver, vê? | vazamento de dados, senha em texto puro |
| Integridade | O dado continua correto e não foi alterado sem permissão? | alteração de registros via SQL Injection |
| Disponibilidade | O sistema está acessível quando precisa? | serviço derrubado, ransomware |

Toda vulnerabilidade afeta pelo menos um pilar. Dizer qual é o primeiro passo para medir o impacto.

## Matriz de risco

Impacto mede o estrago se a falha for explorada. Probabilidade mede a facilidade e a exposição.

| Impacto \ Probabilidade | Baixa | Média | Alta |
|-------------------------|-------|-------|------|
| Baixo | Baixa | Baixa | Média |
| Médio | Baixa | Média | Alta |
| Alto | Média | Alta | Crítica |
| Crítico | Alta | Crítica | Crítica |

Fatores que aumentam a probabilidade: sistema exposto na internet, exploração sem autenticação, técnica conhecida e automatizável.
Fatores que aumentam o impacto: dados pessoais ou financeiros, acesso administrativo, efeito em outros sistemas.

Esta matriz é didática. Em ambientes profissionais é comum usar o CVSS (Common Vulnerability Scoring System) para pontuar vulnerabilidades de forma padronizada.

## Referências que o agente pode citar

- **OWASP Top 10**: lista das categorias de risco mais críticas em aplicações web. SQL Injection está em "Injection".
- **CWE**: catálogo de tipos de fraqueza. Exemplo: CWE-89 (SQL Injection), CWE-79 (XSS), CWE-798 (credenciais no código).
- **MITRE ATT&CK**: base de táticas e técnicas usadas por atacantes. Exemplo: T1190 (Exploit Public-Facing Application), T1110 (Brute Force), T1078 (Valid Accounts).
- **CVE**: identificador de uma vulnerabilidade específica em um produto. Só cite um CVE se tiver certeza do número.

## Boas práticas

**Código**
- Consultas parametrizadas em vez de concatenar entrada do usuário em SQL.
- Validar toda entrada externa no servidor, preferindo listas do que é permitido.
- Senhas com hash forte e lento (bcrypt, scrypt ou argon2), nunca em texto puro.
- Segredos em variáveis de ambiente ou cofre de segredos, nunca no repositório.
- Mensagens de erro genéricas para o usuário e detalhadas só no log interno.
- Dependências atualizadas e auditadas.

**Infraestrutura**
- Menor privilégio: cada usuário e serviço com só o acesso necessário.
- Expor na internet só as portas necessárias; o resto fechado por padrão.
- SSH com chave, sem login direto de root, e MFA onde houver painel administrativo.
- Atualizações de segurança em dia e backups testados.
- Logs centralizados para conseguir investigar um incidente.

**Processo**
- Revisar segurança em cada alteração antes da produção (DevSecOps).
- Testar só em ambientes próprios ou com autorização formal por escrito.
