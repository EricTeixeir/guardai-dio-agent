---
name: security-study-path
description: Use quando o estudante quer começar ou evoluir em cibersegurança e não sabe o que estudar, em que ordem e como praticar com segurança. Monta uma trilha de estudos por fases, com prática em laboratório próprio.
---

# Skill: Trilha de estudos em cibersegurança

Monta uma trilha de estudos em cibersegurança ajustada ao perfil do estudante, com fundamentos, prática em laboratório e marcos de progresso.

## Quando usar

- O estudante quer entrar na área de segurança e não sabe por onde começar.
- Ele terminou uma análise com a skill `vulnerability-analysis` e quer aprofundar o tema.
- Ele está em dúvida entre caminhos (defesa, AppSec, ofensiva, governança).

Se o estudante já escolheu uma experiência específica da DIO e quer só organizar o tempo, use a skill `study-plan`.

## Regras

1. **Prática só em laboratório.** Todo exercício proposto roda em máquinas, contêineres ou plataformas próprias para treino. Nunca proponha praticar em sistemas de terceiros.
2. **Fundamentos antes de ferramentas.** Redes, sistemas operacionais e programação vêm antes de ferramentas ofensivas.
3. **Não invente.** Cite cursos e experiências da DIO pelo nome só se confirmados na conversa ou em https://dio.me. Fora da DIO, indique apenas fontes oficiais e gratuitas (por exemplo, OWASP, MITRE ATT&CK, documentação oficial das ferramentas).

## Processo

### 1. Entenda o perfil

Pergunte, uma coisa por vez, só o que faltar:
- O objetivo: primeiro emprego, migrar de área, proteger o próprio projeto, curiosidade.
- A base atual em redes, Linux e programação.
- O tempo disponível por semana.
- A área de interesse, se já existir. Se a pessoa não souber, apresente os caminhos da etapa 2 em uma frase cada e deixe ela escolher.

### 2. Escolha o caminho

| Caminho | Foco | Bom para quem |
|---------|------|---------------|
| Defesa (Blue Team) | monitoramento, logs, resposta a incidentes, hardening | gosta de infraestrutura e investigação |
| AppSec | código seguro, revisão de código, OWASP Top 10, DevSecOps | já programa ou quer programar |
| Ofensiva (Red Team) | testes de intrusão autorizados, exploração em laboratório | tem base sólida de redes e sistemas |
| Governança (GRC) | políticas, riscos, LGPD, normas como ISO 27001 | gosta de processos e gestão |

### 3. Monte as fases

Organize a trilha em três fases e adapte o conteúdo ao caminho escolhido:

1. **Fundamentos**: tríade CID, ameaça, vulnerabilidade e risco (`agent/knowledge/security-basics.md`), redes (TCP/IP, portas, DNS, HTTP), Linux básico e uma linguagem de script.
2. **Núcleo do caminho**: os temas centrais do caminho escolhido na etapa 2.
3. **Prática e portfólio**: um projeto de laboratório documentado no GitHub (por exemplo, analisar e corrigir um app vulnerável próprio, endurecer um servidor de laboratório, escrever uma regra de detecção).

Para cada fase, indique: o que estudar, um exercício prático em laboratório e uma experiência da DIO para aprofundar (tipo de experiência, ou nome se confirmado).

### 4. Distribua no tempo

Divida as fases em semanas conforme o tempo informado. Constância vale mais que intensidade. Se a estimativa for aproximada, diga isso.

### 5. Defina marcos

Inclua um marco verificável por fase (por exemplo: "ao fim da fase 1, você explica a diferença entre ameaça e vulnerabilidade com um exemplo seu").

### 6. Entregue e ajuste

Apresente a trilha e pergunte se o ritmo cabe na rotina do estudante. Ajuste conforme a resposta.

## Formato de saída

- Perfil e caminho escolhido, em duas linhas.
- Tabela com fase, conteúdo, prática em laboratório, experiência da DIO e duração.
- Marcos por fase.
- Primeiro passo concreto para começar hoje.

## Lembre-se

- Segurança se aprende fazendo, mas sempre no próprio laboratório.
- A trilha deve caber na vida real do estudante.
- Combine com `vulnerability-analysis` para praticar e com `explain-concept` para dúvidas pontuais.
