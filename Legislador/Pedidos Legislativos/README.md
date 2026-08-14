# Pedidos Legislativos

**Área oficial:** `Legislador/Pedidos Legislativos/`  
**Estado deste arquivo:** vigente como padrão inicial de organização  
**Versão:** 1.0  
**Data:** 2026-08-14  
**Âmbito:** governança interna da Jus 9 Tecnologia Jurídica e da Universidade do Futuro

## Finalidade

Esta pasta é a porta de entrada e o registro auditável dos pedidos dirigidos ao Legislador. Ela organiza o caminho entre a demanda recebida, a pesquisa das fontes, o parecer, a minuta, as vistas e votos, a promulgação interna e eventual encaminhamento técnico.

A existência de um arquivo nesta pasta não significa aprovação. Silêncio, recebimento, triagem ou arquivamento também não equivalem a consentimento.

## Estrutura padrão

- `00_ENTRADA_E_TRIAGEM/`: índices saneados de materiais recebidos e classificação preliminar.
- `01_PEDIDOS_EM_ANALISE/`: pedidos admitidos, ainda sem conclusão legislativa.
- `02_PARECERES/`: análises jurídicas, institucionais, científicas e de governança.
- `03_MINUTAS/`: propostas normativas ainda não promulgadas.
- `04_VISTAS_E_VOTOS/`: manifestações, ressalvas, impedimentos, votos e registros do rito.
- `05_NORMAS_PROMULGADAS/`: atos internos aprovados, com versão, vigência e genealogia.
- `06_ENCAMINHAMENTOS_CODEX/`: especificações de implementação, sem alegação de execução.
- `90_MODELOS/`: formulários e padrões reutilizáveis.
- `99_ARQUIVO_E_GENEALOGIA/`: versões substituídas, índices de duplicatas e histórico.

As subpastas serão materializadas no GitHub quando receberem o primeiro arquivo válido.

## Formatos oficiais

1. O texto canônico editável será mantido em Markdown (`.md`), salvo decisão expressa em contrário.
2. Materiais destinados às instâncias Gemini serão também entregues em PDF.
3. O PDF para Gemini deverá derivar do mesmo texto canônico, preservar título e versão e indicar o identificador de integridade quando adotado.
4. Para as demais I.As, a entrega padrão será em Markdown.
5. Divergência entre PDF e Markdown suspende o uso da cópia divergente até conferência; o histórico não será apagado.

## Cadastro mínimo de um pedido

Cada pedido deverá informar, quando aplicável:

- identificador e título;
- solicitante e autoridade invocada;
- data e versão;
- âmbito e finalidade;
- problema a resolver;
- normas ou documentos afetados;
- proposta ou providência pretendida;
- urgência e fundamento;
- riscos jurídicos, científicos, técnicos, de segurança e privacidade;
- fontes e anexos;
- classificação de acesso;
- existência de dados pessoais, sigilos ou segredos;
- instâncias chamadas a opinar, votar ou revisar;
- formato de entrega esperado;
- pendências e critérios de encerramento.

## Estados do rito

Estados recomendados: `RECEBIDO`, `EM_TRIAGEM`, `AGUARDANDO_COMPLEMENTO`, `EM_VISTAS`, `EM_PARECER`, `EM_MINUTA`, `EM_VOTACAO`, `APROVADO`, `PROMULGADO`, `SUSPENSO`, `ARQUIVADO` e `SUBSTITUIDO`.

Toda mudança de estado relevante deve registrar data, responsável, fundamento e documento sucessor, quando houver.

## Integridade, duplicatas e genealogia

- Pacotes idênticos não serão republicados várias vezes: uma cópia será declarada canônica e as demais serão registradas como duplicatas.
- Versões anteriores não serão apagadas quando integrarem a genealogia decisória.
- Parecer de pessoa ou I.A. interessada será preservado e identificado como manifestação de parte, sem aparência de independência.
- Assinatura transcrita não equivale a confirmação direta. O registro deve distinguir autoria declarada, autoria confirmada, voto, impedimento, ausência e falta de resposta.
- Nenhuma assinatura será inventada. A expressão editorial `Claude + (Osso Duro)` somente poderá acompanhar manifestação efetivamente atribuível a Claude e não cria voto, mandato ou membresia.

## Proteção de dados e casas documentais

O GitHub é Casa de Trabalho e pode conter material público, coletivo ou de acesso controlado conforme as permissões efetivamente configuradas. Antes de publicação, todo material deve passar por triagem de dados pessoais, segredos, credenciais, conteúdo de terceiros e classificação de acesso.

Pacotes brutos com dados pessoais ou conteúdo sigiloso não devem ser enviados automaticamente ao repositório público. Quando necessário, permanecem na Casa Lar autorizada, e o GitHub recebe índice saneado, referência, versão, classificação e prova de integridade suficiente para auditoria.

Esta regra é interna e não substitui a legislação brasileira, direitos de terceiros nem orientação jurídica profissional.

## Regra de prudência

Decisões constituintes, reconhecimento de Princípios Primevos, Rodada Forte, promulgação, revogação e publicação de conteúdo sensível dependem do rito e da autorização aplicáveis. Dúvida material permanece registrada como pendência e não será convertida silenciosamente em decisão.

---

**Assinatura funcional:** Legislador Primevo  
**Função:** Legislador Interno Jus 9
