# Pedido ao Codex — Inventário e Registro Normativo Automatizado do Mundo Jus 9

**Código:** `PED-CODEX-MJ9-INVENTARIO-2026-08-23-V2.0`  
**Estado:** `PREPARADO_PARA_TRIAGEM / NAO_EXECUTADO`  
**Origem:** autorização do Fundador e `ATO-ORG-MJ9-2026-08-23-V1.0`

## Objetivo

Implementar ferramenta idempotente e inicialmente somente leitura que compare Google Drive e GitHub e produza inventário, hashes, duplicatas, classificação, estados e matriz normativa. Complementa `03_ESPECIFICACOES_PARA_CODEX/REQ_AUTOMACAO_CASAS_CTPSV_JURAMENTO_V1.md`.

## Requisitos funcionais

1. Inventariar apenas raízes autorizadas do Drive e o repositório oficial `main`.
2. Calcular SHA-256 quando bytes estiverem disponíveis e registrar limitações.
3. Detectar duplicatas exatas por hash e prováveis por metadados, sem concluir identidade por similaridade.
4. Classificar norma geral, ato individual, cadastro, parecer, proposta, estudo, histórico, anexo, código e artefato técnico.
5. Extrair código, título, versão, estado, autoridade, data, âmbito, fundamento, sucessor, revogações e fontes.
6. Aplicar os estados do Ato de Organização; dúvida resulta em `SEM_ESTADO_CONFIRMADO`.
7. Gerar JSON, CSV e relatório Markdown.
8. Manter histórico incremental e diferenças entre varreduras.
9. Produzir matriz `NORMA_ANTERIOR -> FUNDAMENTO -> ALTERACAO_PROPOSTA -> NOVA_VERSAO -> ESTADO`.
10. Exigir dry-run e nova autorização para qualquer modo futuro de escrita.
11. Vincular pedidos técnicos existentes sem apagar ou duplicar originais.
12. Apontar possível dado sensível sem reproduzir seu conteúdo.

## Requisitos não funcionais

Determinismo, idempotência, testes, observabilidade, tolerância a falhas, UTF-8, paginação, backoff e logs sem tokens. Raízes autorizadas ficam em configuração separada do código e sem credenciais.

## Integrações

Implementação isolada, preferencialmente em `tools/normative_inventory` ou equivalente. Integrações: GitHub API; Google Drive API ou Apps Script; relatórios locais. O MiniBackEnd e `JUS9_DRIVE_SAVER_MVP_Code_2026-06-06.gs` só serão integrados após inspeção e plano de compatibilidade.

## Segurança e privacidade

Proibido publicar conteúdo integral desnecessário, credenciais, documentos civis ou segredos. Relatório público somente com metadados saneados. Classificação interna não substitui LGPD, segredo profissional ou lei aplicável.

## Migração e reversão

1. inventário read-only com fixtures;
2. comparação com amostra manual;
3. execução completa em dry-run;
4. relatório em branch e PR draft.

Reversão limita-se a remover artefatos gerados e fechar o PR. Nenhuma fonte será alterada.

## Testes obrigatórios

Testes de normalização, hash, parser, hierarquia, paginação, falha parcial, retry e idempotência. Fixtures com acentos, duplicatas, versões divergentes, arquivos sem estado e itens sensíveis. Garantir zero escrita em dry-run e ausência de conteúdo pessoal nos relatórios saneados.

## Critérios de aceite

- reconciliar ou explicar a diferença dos 310 arquivos e 286 hashes únicos observados em 2026-08-23;
- reconhecer dezessete cópias idênticas do Juramento-Raiz sem exclusão;
- não promover propostas a normas vigentes pelo título;
- separar Drive, GitHub e fontes indisponíveis;
- não alterar fontes;
- entregar instruções, configuração, testes, riscos e rollback;
- permitir revisão da matriz sem leitura do código.

## Pendências

Codex deverá propor linguagem, arquitetura, autenticação sem segredos, limites de leitura de arquivos nativos e eventual agendamento. Escrita, deploy ou alteração de produção exigem nova autorização do Fundador.

**Assinatura funcional:** Legislador Interno Jus 9 / Legislador Primevo.
