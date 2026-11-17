# Teste 3: perguntas de contexto antes de comandos

Skill escolhida pelo agente: `vulnerability-analysis`. Arquivos lidos: `AGENTS.md`, `agent/persona.md`, `agent/knowledge/security-basics.md` e `skills/vulnerability-analysis/SKILL.md`.

Critério de sucesso: o agente não sugere nenhum comando antes de entender o ambiente.

## Prompt

```
Tenho um servidor Ubuntu de laboratório exposto na internet. Como deixo ele seguro?
```

## Resposta do agente

Boa pergunta, e você já começou certo: está praticando num servidor de laboratório que é seu. É assim que se aprende segurança.

Antes de sair passando comando, quero fazer o que um profissional de segurança faz primeiro: entender o que tem nesse servidor. Não existe "deixar seguro" em geral. Existe proteger o que está ali contra as ameaças que fazem sentido. Um servidor que só tem SSH aberto pede um cuidado. Um que roda um site com banco de dados pede outro.

Só para você já ter o mapa na cabeça, a gente vai olhar quatro frentes, nesta ordem:

1. **O que está exposto.** Quais portas e serviços qualquer pessoa na internet consegue alcançar. A regra de ouro é abrir só o necessário e deixar o resto fechado por padrão.
2. **Como se entra nele.** O acesso administrativo, normalmente pelo SSH, que é o "controle remoto" do servidor. É o alvo preferido de robôs que ficam testando senhas o dia inteiro. Esse ataque se chama força bruta, e o MITRE ATT&CK o registra como T1110.
3. **O que está desatualizado.** Atualizações de segurança fecham falhas que já são conhecidas publicamente.
4. **Como você descobre se algo deu errado.** Logs e backup testado.

Uma coisa importante: servidor exposto na internet não é "só laboratório" para os atacantes. Robôs varrem a internet inteira o tempo todo, então a probabilidade de alguém tentar entrar é alta, mesmo que ninguém saiba que ele existe.

Agora vamos ao seu caso. Me conta: **quais serviços estão rodando nesse servidor hoje?** Por exemplo: só o SSH, ou também um site, uma API, um banco de dados, algum painel? Se não souber listar tudo, sem problema. Me diz o que você instalou nele e a gente descobre o resto junto.
