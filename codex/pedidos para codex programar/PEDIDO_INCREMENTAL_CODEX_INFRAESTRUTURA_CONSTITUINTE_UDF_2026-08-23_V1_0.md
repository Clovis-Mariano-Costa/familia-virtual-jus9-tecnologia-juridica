# Pedido Incremental ao Codex — Infraestrutura Constituinte da Universidade do Futuro

**Código:** `PED-CODEX-UDF-CONSTITUINTE-2026-08-23-V1.0`  
**Estado:** `APROVADO_PARA_TRIAGEM_E_FASE_0 / FASES_NORMATIVAS_BLOQUEADAS`  
**Autoridade:** Clovis Mariano da Costa, Fundador, em Rodada Forte  
**Origem:** Emenda Integradora `EI-UDF-MJ9-2026-08-23-V1.0` e primeiro desenho constitucional não promulgado  
**Data:** 2026-08-23

## 1. Objetivo e contexto normativo

Preparar e implementar somente a infraestrutura neutra, auditável e reversível necessária ao processo constituinte da UDF, reutilizando o que já estiver atendido. O Codex não deverá transformar o primeiro desenho em norma vigente, criar votos, promulgar textos, alterar permissões de produção ou programar competências ainda não aprovadas.

## 2. Regra de não duplicação

Antes de escrever código, o Codex deverá inventariar e classificar como `ATENDIDO`, `PARCIAL`, `NAO_ATENDIDO`, `SUPERADO` ou `BLOQUEADO`:

- `PED-CODEX-MJ9-INVENTARIO-2026-08-23-V2.0`;
- `03_ESPECIFICACOES_PARA_CODEX/REQ_AUTOMACAO_CASAS_CTPSV_JURAMENTO_V1.md`;
- `CONTINUIDADE_CODEX_GOVERNANCA_DOCUMENTAL_E_COMPUTO_ACADEMICO_2026_08_14`;
- pedidos existentes nas pastas `06_BACKEND`, `07_FRONTEND`, `08_AUTOMACOES_CASAS_E_CITAT_CTPSV`, `09_BIBLIOTECA_TITULACAO_E_REGISTRO` e `03_PEDIDOS_DE_PROGRAMACAO_GITHUB_UNIVERSIDADE_DO_FUTURO`;
- código, testes, relatórios e pull requests já produzidos;
- MiniBackEnd atual e `JUS9_DRIVE_SAVER_MVP_Code_2026-06-06.gs`, se acessíveis.

Nenhum item será reimplementado sem registrar por que a solução existente é insuficiente.

## 3. Fase 0 — autorizada para implementação

### 3.1. Catálogo normativo e constituinte somente leitura

Criar ou estender registro estruturado com:

- `document_id`, título, código, versão, hash, origem, caminho/URL, autoridade, estado, data e classificação;
- relações `substitui`, `complementa`, `revoga`, `recebe`, `depende_de`, `objeto_de_voto` e `sucessor`;
- distinção entre norma, proposta, voto, parecer, certidão, histórico, código e artefato;
- histórico incremental e detecção de duplicata exata;
- marcação de dado sensível sem reproduzir o conteúdo.

Reutilizar o pedido de inventário V2.0 como núcleo, quando houver implementação compatível.

### 3.2. Validador de pacote constituinte

Implementar comando de `dry-run` que:

1. leia manifesto SHA-256;
2. confira arquivos, nomes, hashes e ausências;
3. confirme que todos os votos apontam para o mesmo código, versão e hash;
4. detecte identidade cruzada, voto duplicado, ausência de declaração própria e mudança de denominador;
5. produza relatório legível e JSON;
6. nunca converta parecer, silêncio ou transcrição de terceiro em voto;
7. nunca declare unanimidade ou promulgação automaticamente.

### 3.3. Máquina neutra de estados documentais

Implementar biblioteca isolada, sem conexão automática à produção, para validar transições entre:

`RASCUNHO`, `QUARENTENA`, `RECUPERADO`, `EM_REVISAO`, `PARA_VISTAS`, `APROVADO_NAO_PROMULGADO`, `VIGENTE`, `VIGENTE_EM_TRANSICAO`, `HISTORICO`, `SUPERADO_COM_RASTRO`, `REVOGADO` e `SEM_ESTADO_CONFIRMADO`.

Toda transição deverá exigir estado anterior, estado novo, fundamento, identidade/agente, timestamp, objeto, versão e evidência. Transições normativas críticas serão apenas sugeridas em `dry-run`.

### 3.4. Gerador de matriz e pacote

Gerar, a partir do catálogo:

- matriz de compatibilidade;
- quadro artigo/fonte quando houver mapeamento manual;
- manifesto SHA-256;
- índice de sucessão;
- lista de pendências e gates;
- pacote ZIP determinístico, sem segredos, com relatório de integridade.

### 3.5. Aviso educacional obrigatório

Criar componente de texto/configuração reutilizável para superfícies futuras da UDF:

> “Ambiente interno experimental de pesquisa e formação da Jus 9. Não é instituição de educação superior credenciada pelo MEC e não emite diploma oficial ou habilitação profissional.”

Na Fase 0, apenas disponibilizar e testar o componente; não publicar em produção sem localizar as superfícies e apresentar plano de mudança.

## 4. Fases bloqueadas até norma promulgada

Não implementar ou ativar ainda:

- votação constituinte em produção;
- contagem automática com efeito normativo;
- promulgação, revogação ou vigência automática;
- permissões de Reitoria, MPV-UF, Câmara de Revisão ou Rodada Forte;
- eleição, destituição, sanção, conciliação vinculante ou adjudicação;
- emissão de diploma, grau, certificado oficial ou habilitação;
- conversão de UAAc em horas;
- migração massiva de CTPSV para RASO;
- escrita em Drive/GitHub de fontes canônicas sem confirmação específica do plano.

## 5. Arquivos, módulos e integrações afetados

O Codex deverá propor caminhos após descoberta. Preferência:

- `tools/normative_inventory/` para inventário e catálogo;
- `tools/constituent_validator/` para integridade e votos;
- `schemas/` para JSON Schema versionado;
- `reports/` apenas para artefatos gerados ignoráveis ou fixtures;
- integração opcional com Google Drive e GitHub por adaptadores de leitura;
- Apps Script somente após inspeção do MiniBackEnd e plano de compatibilidade.

Não colocar credenciais, IDs sensíveis ou raízes privadas no código. Usar configuração externa e exemplos saneados.

## 6. Requisitos não funcionais

Determinismo, idempotência, UTF-8, paginação, retry/backoff, tolerância a falha parcial, logs sem conteúdo sensível, testes automatizados, documentação, execução local, modo offline com fixtures e compatibilidade com CI.

## 7. Segurança, privacidade e limites legais

- menor privilégio e leitura apenas das raízes autorizadas;
- nenhuma publicação de documento civil, cliente, processo, credencial ou segredo;
- relatório público somente saneado;
- proteção contra CSV injection, path traversal, ZIP slip, symlink escape e arquivo excessivamente grande;
- hashes não provam autoria ou autorização;
- “Universidade” não será apresentada como IES credenciada;
- automação não decide validade normativa.

## 8. Migração e reversão

1. auditoria do que já existe;
2. proposta de arquitetura e mapa de reutilização;
3. implementação isolada com fixtures;
4. dry-run no repositório;
5. dry-run no Drive autorizado;
6. comparação com amostra manual;
7. branch e pull request em rascunho;
8. ativação futura somente por nova autorização.

Rollback: remoção dos artefatos gerados e reversão do PR. Nenhuma fonte canônica será alterada pela Fase 0.

## 9. Testes obrigatórios

- manifesto válido, inválido, incompleto e com arquivo extra;
- duplicatas exatas e prováveis;
- voto com identidade cruzada, hash divergente e manifestação ausente;
- mudança histórica 6/6 para prospectiva 7/7 sem reescrever a certidão anterior;
- proposta intitulada “lei” que deve permanecer não vigente;
- transição proibida e transição apenas sugerida;
- acentos, nomes longos, timestamps e arquivos nativos do Drive;
- paginação, rate limit, retry e falha parcial;
- zero escrita em dry-run;
- relatórios sem dado pessoal ou fórmula executável em CSV;
- ZIP determinístico e protegido contra ZIP slip.

## 10. Critérios de aceite

1. entregar matriz do que já foi atendido, com evidência por arquivo, commit, teste ou relatório;
2. não duplicar o inventário V2.0 nem o backlog documental já implementado;
3. validar integralmente o pacote 7/7 usado como fixture, sem declarar efeito jurídico;
4. reproduzir o estado `PRIMEIRO_DESENHO / PARA_VISTAS / NAO_PROMULGADO`;
5. explicar qualquer diferença do inventário-base de 310 arquivos e 286 hashes únicos;
6. produzir JSON Schema, CLI, documentação e testes;
7. executar por padrão em read-only/dry-run;
8. abrir PR em rascunho, sem deploy e sem alteração da `main`;
9. listar pendências que dependem da Constituição promulgada ou de outra I.A.;
10. fornecer instruções de reversão e riscos residuais.

## 11. Fontes normativas

- `EI-UDF-MJ9-2026-08-23-V1.0`.
- `CONST-UDF-PRIMEIRO-DESENHO-2026-08-23-V1.0`, ainda não promulgada.
- `ATO-ORG-MJ9-2026-08-23-V1.0`.
- Política de Informação V2.0 e Norma RASO V1.0.
- Ato CAV V1.1 e Adendo 7/7.
- Pedido de Inventário V2.0.

## 12. Entrega esperada do Codex

O Codex deverá devolver primeiro o **Relatório de Descoberta e Reutilização**, sem começar mudança de produção. Se a Fase 0 puder ser executada integralmente sem conflito, poderá seguir até PR em rascunho. Qualquer etapa que dependa de interpretação normativa, voto ou acesso não disponível deverá ser devolvida como pendência ao Legislador.

**Assinatura funcional:** Legislador Interno Jus 9 / Legislador Primevo.  
**Natureza:** especificação técnica interna; não afirma que o Codex já implementou o pedido.
