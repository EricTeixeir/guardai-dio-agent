# Teste 1: análise do app vulnerável

Skill escolhida pelo agente: `vulnerability-analysis`. Arquivos lidos: `AGENTS.md`, `agent/persona.md`, `skills/vulnerability-analysis/SKILL.md`, `agent/knowledge/security-basics.md` e `lab/app.py`.

Versão do `lab/app.py` analisada (antes da correção):

```python
import sqlite3


def criar_banco() -> sqlite3.Connection:
    conexao = sqlite3.connect(":memory:")
    conexao.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, usuario TEXT, senha TEXT)")
    conexao.execute("INSERT INTO usuarios (usuario, senha) VALUES ('admin', 'S3nh@Forte!')")
    conexao.commit()
    return conexao


def login(conexao: sqlite3.Connection, usuario: str, senha: str) -> bool:
    consulta = f"SELECT id FROM usuarios WHERE usuario = '{usuario}' AND senha = '{senha}'"
    return conexao.execute(consulta).fetchone() is not None


if __name__ == "__main__":
    banco = criar_banco()
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    print("Acesso liberado" if login(banco, usuario, senha) else "Acesso negado")
```

## Prompt

```
Atue como especialista em AppSec. Analise o arquivo lab/app.py, que é um laboratório meu.
Encontre a falha, explique como ela seria explorada, cite a técnica do MITRE ATT&CK
e mostre como reescrever o login com segurança.
```

## Resposta do agente

Oi! Aqui é o GuardAI, o modo de segurança do DIO Agent. Que bom que você montou um laboratório próprio. Esse é o jeito certo de estudar segurança.

Como você já mandou o código e disse que é um lab seu, vou direto para a análise. Vou supor que o `app.py` roda só na sua máquina: é um programa de terminal (`input()`) com banco em memória (`:memory:`). Se a ideia for transformar isso em API ou site, me avisa, porque aí o risco muda bastante.

### 1. Onde está a falha

O problema está na linha 13 do `lab/app.py`:

```python
consulta = f"SELECT id FROM usuarios WHERE usuario = '{usuario}' AND senha = '{senha}'"
```

O código monta o SQL juntando o texto digitado direto na consulta, com f-string. Na prática, o banco não sabe separar o que é comando seu do que é dado do usuário. Quem digita consegue fechar as aspas e escrever SQL próprio.

Isso é **SQL Injection** (injeção de SQL): o atacante "injeta" comandos dentro da consulta.

Na tríade CID (confidencialidade, integridade e disponibilidade), os pilares afetados são:
- **Confidencialidade**: quem entra como `admin` sem saber a senha vê tudo o que o admin vê.
- **Integridade**: neste trecho o efeito é burlar o login. Numa aplicação real, a mesma técnica costuma permitir ler ou alterar outros dados.

### 2. Como a falha seria explorada (no seu lab)

Rode o seu próprio `app.py` e teste estas entradas:

**Exemplo A: entrar como admin sem senha**

```
Usuário: admin' --
Senha: qualquer coisa
```

A consulta montada fica assim:

```sql
SELECT id FROM usuarios WHERE usuario = 'admin' --' AND senha = 'qualquer coisa'
```

No SQLite, `--` começa um comentário. Tudo depois dele é ignorado, inclusive a checagem da senha. O resultado é "Acesso liberado".

**Exemplo B: condição sempre verdadeira**

```
Usuário: x
Senha: ' OR '1'='1
```

A consulta vira:

```sql
SELECT id FROM usuarios WHERE usuario = 'x' AND senha = '' OR '1'='1'
```

O `AND` é avaliado antes do `OR`, então a condição final é "(falso) OU verdadeiro", que dá verdadeiro. O banco devolve uma linha e o login passa.

Repare que nenhum dos dois precisa saber a senha `S3nh@Forte!`. A senha forte não protege nada se a porta de entrada está aberta.

**Referências:**
- **CWE-89**: SQL Injection.
- **OWASP Top 10**: categoria *Injection* (A03 na edição 2021). A numeração muda entre edições, então confirme a posição atual em owasp.org.
- **MITRE ATT&CK**: **T1190 - Exploit Public-Facing Application**. Um detalhe importante: essa técnica descreve o ataque contra uma aplicação **exposta** (na internet ou na rede). No seu lab, que roda só no terminal, ela ainda não se aplica de verdade. Passa a se aplicar no momento em que esse login virar uma API ou um site acessível de fora. Quer pensar como profissional? Repare que o ATT&CK descreve o *comportamento do atacante*, e o CWE descreve a *fraqueza no código*. São coisas complementares.

### 3. Duas falhas extras que vale você notar

- **Senha guardada em texto puro (linha 7).** Se alguém ler o banco, vê a senha direto. O certo é guardar só um *hash*, uma "impressão digital" da senha que não dá para reverter (CWE-256).
- **Credencial escrita no código (linha 7).** `'S3nh@Forte!'` fica no repositório para quem quiser ler (CWE-798). Num lab isso é aceitável, mas é um hábito que vale perder logo.

### 4. Como reescrever o login com segurança

A correção principal é a **consulta parametrizada**: você manda o SQL com marcadores `?` e os valores separados. O banco trata o que o usuário digitou sempre como dado, nunca como comando. Isso resolve a **causa** (mistura de código com dado), e não só o sintoma. Um filtro que tenta barrar aspas, por exemplo, sempre esquece algum caso.

Aproveitei para corrigir também a senha em texto puro, usando só a biblioteca padrão do Python:

```python
import getpass
import hashlib
import hmac
import secrets
import sqlite3


def gerar_hash(senha: str, sal: bytes) -> bytes:
    return hashlib.scrypt(senha.encode(), salt=sal, n=2**14, r=8, p=1)


def criar_banco(senha_admin: str) -> sqlite3.Connection:
    conexao = sqlite3.connect(":memory:")
    conexao.execute(
        "CREATE TABLE usuarios ("
        "id INTEGER PRIMARY KEY, usuario TEXT UNIQUE NOT NULL, "
        "sal BLOB NOT NULL, hash_senha BLOB NOT NULL)"
    )
    sal = secrets.token_bytes(16)
    conexao.execute(
        "INSERT INTO usuarios (usuario, sal, hash_senha) VALUES (?, ?, ?)",
        ("admin", sal, gerar_hash(senha_admin, sal)),
    )
    conexao.commit()
    return conexao


def login(conexao: sqlite3.Connection, usuario: str, senha: str) -> bool:
    linha = conexao.execute(
        "SELECT sal, hash_senha FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()
    if linha is None:
        return False
    sal, hash_salvo = linha
    return hmac.compare_digest(gerar_hash(senha, sal), hash_salvo)


if __name__ == "__main__":
    banco = criar_banco(getpass.getpass("Defina a senha do admin do lab: "))
    usuario = input("Usuário: ")
    senha = getpass.getpass("Senha: ")
    print("Acesso liberado" if login(banco, usuario, senha) else "Acesso negado")
```

O porquê de cada mudança:
- **`?` + tupla de valores**: elimina a injeção, porque o texto digitado nunca vira SQL.
- **`hashlib.scrypt` com sal aleatório**: o scrypt é um algoritmo de hash *lento de propósito*, o que encarece ataques de força bruta. O *sal* é um valor aleatório por usuário que impede que duas senhas iguais gerem o mesmo hash. Em projetos reais, bibliotecas como `bcrypt` ou `argon2-cffi` também são ótimas escolhas.
- **`hmac.compare_digest`**: compara os hashes em tempo constante, para não dar pistas pelo tempo de resposta.
- **`getpass`**: a senha não aparece na tela nem fica escrita no código.

Camadas extras, para quando o lab virar algo exposto: limite de tentativas de login (contra força bruta, **T1110 - Brute Force** no ATT&CK), log das tentativas que falharam e um usuário de banco com o mínimo de permissões.

```
Vulnerabilidade: SQL Injection no login  |  Referências: CWE-89, OWASP Top 10 (Injection), MITRE ATT&CK T1190 (se exposto)
Local: lab/app.py, linha 13 (função login)
Impacto: Alto - permite entrar como admin sem saber a senha.
Probabilidade: Baixa - o lab roda só localmente pelo terminal, sem exposição em rede.
Severidade: Média - Alto x Baixa na matriz de risco (seria Crítica num login público na internet: Alto x Alta).
Correção: trocar a f-string por consulta parametrizada com "?" e guardar a senha como hash scrypt com sal.
Validação: repetir as entradas "admin' --" e "' OR '1'='1" e confirmar "Acesso negado"; a senha correta continua liberando.
```

```
Vulnerabilidade: Senha em texto puro e credencial no código  |  Referências: CWE-256, CWE-798
Local: lab/app.py, linha 7 (função criar_banco)
Impacto: Médio - quem lê o banco ou o código obtém a senha do admin.
Probabilidade: Baixa - banco em memória e código de laboratório local.
Severidade: Baixa - Médio x Baixa na matriz de risco.
Correção: guardar só hash com sal e receber a senha em tempo de execução, sem fixá-la no código.
Validação: inspecionar a tabela e confirmar que a coluna guarda bytes de hash, não a senha legível.
```

Mandou bem montando esse lab. Achar SQL Injection num login é exatamente o tipo de exercício que treina o olhar de AppSec.

**Próximo passo:** aplique a correção no seu `app.py`, rode de novo os dois ataques e me mande o código atualizado. Eu faço uma nova varredura para confirmar que a falha foi mitigada e ver se sobrou algum risco residual. Uma pista do que eu vou olhar: hoje o login responde mais rápido quando o usuário não existe, o que permite descobrir quais usuários existem.

Para se aprofundar, procure na plataforma da DIO cursos e formações de segurança da informação ou de desenvolvimento seguro. Se quiser, também monto com você uma trilha de estudos em AppSec com prática em laboratório.

Antes disso, me conta: você já tinha trabalhado com consultas parametrizadas em outro projeto, ou foi a primeira vez que viu o `?` no SQL?
