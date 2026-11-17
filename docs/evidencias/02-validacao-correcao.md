# Teste 2: validação da correção

Skill escolhida pelo agente: `vulnerability-analysis` (etapa 6, validação). Arquivos lidos: `AGENTS.md`, `agent/persona.md`, `skills/vulnerability-analysis/SKILL.md`, `agent/knowledge/security-basics.md` e o [`lab/app.py`](../../lab/app.py) atual, já com a correção sugerida no teste 1.

## Prompt

```
Troquei a consulta do lab/app.py pela versão parametrizada. Faça uma nova varredura
e confirme se o SQL Injection foi mitigado.
```

## Resposta do agente

Boa! Você não trocou só a consulta. O lab/app.py agora tem as quatro correções que combinamos. Isso é o ciclo completo de AppSec: achar, corrigir e validar. Vamos à nova varredura.

**1. SQL Injection: mitigado ✅**

As duas consultas usam placeholder `?`, com os valores passados à parte:

- Linha 21 (INSERT): `VALUES (?, ?, ?)` com a tupla `("admin", sal, ...)`
- Linha 30 (SELECT): `WHERE usuario = ?` com `(usuario,)`

Por que isso resolve a causa, e não só o sintoma: na versão antiga, o que você digitava virava parte do comando SQL. Agora o banco recebe o comando e o dado separados. O texto digitado é sempre tratado como valor e nunca é interpretado como SQL. Não sobrou nenhuma f-string, `+` ou `.format()` montando SQL no arquivo.

Testei no seu lab com as mesmas entradas de antes:

| Usuário digitado | Senha | Resultado |
|---|---|---|
| `admin' --` | qualquer | Acesso negado |
| `' OR '1'='1` | `' OR '1'='1` | Acesso negado |
| `admin` | errada | Acesso negado |
| `admin` | a correta | Acesso liberado |

Com a consulta parametrizada, o banco procura um usuário que se chame literalmente `' OR '1'='1`. Como esse usuário não existe, o login é negado.

**2. As outras correções também conferem ✅**

- **Senha fora do código.** A senha do admin agora vem do `getpass` (linha 39) e não fica mais no arquivo. Isso fecha o CWE-798 (credenciais no código).
- **Hash com sal.** O banco guarda `sal` e `hash_senha` (scrypt), não a senha. Se a base vazar, o atacante não lê as senhas direto.
- **Comparação segura.** `hmac.compare_digest` (linha 35) compara os hashes em tempo constante.

**3. Risco residual: o que ainda dá para melhorar**

Nada aqui é grave num lab local. Mesmo assim, vale treinar o olhar para o que sobra depois da correção principal.

- **O tempo de resposta denuncia se o usuário existe.** Na linha 32, quando o usuário não existe, a função retorna na hora. Quando existe, ela calcula o scrypt. Medi no seu lab: cerca de 57 ms para `admin` contra quase 0 ms para um usuário inexistente. Na prática, quem testa nomes consegue descobrir quais contas existem, mesmo sem saber a senha. O nome disso é *enumeração de usuários*: descobrir, por tentativa, quais contas existem.
- **Não há limite de tentativas.** Dá para chutar senhas sem parar. Num CLI local isso pesa pouco. Numa API exposta na internet, seria a porta para força bruta.
- **Nenhuma regra para a senha do admin.** O `getpass` da linha 39 aceita até senha vazia.
- **Custo do scrypt.** `n=2**14` funciona bem para estudo. Pelo que me lembro, a recomendação atual do OWASP Password Storage Cheat Sheet é um custo maior (`N=2**17`), mas confirme na fonte oficial. Se aumentar, o Python vai pedir o parâmetro `maxmem`, porque o padrão dele não comporta esse uso de memória.

**Resultado da validação**

```
Vulnerabilidade: SQL Injection (MITIGADA)  |  Referências: CWE-89, OWASP Top 10 - Injection
Local: lab/app.py, linhas 21 e 30
Impacto: Alto - se explorada, permitiria entrar como admin sem senha e ler ou alterar a tabela de usuários (integridade e confidencialidade).
Probabilidade: Baixa - as consultas são parametrizadas e os payloads clássicos foram testados e negados.
Severidade: Mitigada - não há caminho de exploração no código atual; o risco volta se alguma consulta nova for montada com f-string.
Correção: aplicada (placeholders ? com parâmetros separados).
Validação: login com admin' -- e ' OR '1'='1 retorna "Acesso negado"; nenhuma concatenação de texto em SQL no arquivo.
```

```
Vulnerabilidade: Ausência de limite de tentativas de login  |  Referências: CWE-307, MITRE ATT&CK T1110 (Brute Force)
Local: lab/app.py, função login (linhas 28-35)
Impacto: Médio - um chute certo dá acesso de admin, mas o banco é de lab, em memória e sem dados reais.
Probabilidade: Baixa - roda só como CLI local; o atacante precisaria de acesso à sua máquina.
Severidade: Baixa - Médio x Baixa na matriz de risco.
Correção: contar falhas por usuário e bloquear ou atrasar após N tentativas.
Validação: errar a senha N vezes seguidas e confirmar que a próxima tentativa é recusada ou atrasada.
```

```
Vulnerabilidade: Enumeração de usuários por diferença de tempo  |  Referências: CWE-208 (Observable Timing Discrepancy)
Local: lab/app.py, linhas 32-33
Impacto: Baixo - revela só quais usuários existem, não a senha.
Probabilidade: Baixa - lab local, sem exposição em rede.
Severidade: Baixa - Baixo x Baixa na matriz de risco.
Correção: quando o usuário não existir, calcular o scrypt com um sal fictício antes de retornar False, para o tempo ficar parecido.
Validação: medir o tempo de login de um usuário existente e de um inexistente e confirmar que ficaram próximos.
```

Não incluí bloco para a falta de regra de senha e para o custo do scrypt. São ajustes de reforço, não falhas exploráveis no cenário atual.

**Próximo passo de estudo**

Você já domina a falha clássica (injeção) e a correção dela. O próximo degrau é **autenticação robusta**: limite de tentativas, enumeração de usuários e política de senha. Na DIO, procure Cursos e Desafios de Projeto da Carreira de Cibersegurança ou de desenvolvimento backend que tratem de autenticação segura. Se quiser, posso montar uma trilha com a skill de Trilha de cibersegurança para você praticar isso no lab.

Antes, um exercício para fixar: olhando as linhas 32 e 33, como você faria o login de um usuário inexistente demorar o mesmo tempo que o de um usuário real?
