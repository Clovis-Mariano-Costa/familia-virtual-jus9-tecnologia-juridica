# Matriz Operacional de Gates Acadêmicos da Universidade do Futuro

**Código:** `MAT-GATE-UDF-2026-08-23-V1.0`  
**Norma de origem:** `NGA-DOC-UDF-2026-001-V1.0`  
**Estado:** `VIGENTE`  
**Data:** 2026-08-23 — America/Sao_Paulo

| Entrada e gate | Responsável | Evidência e resultado |
|---|---|---|
| `RASCUNHO` — aceitação da fonte | autor e orientador | Markdown, autoria, versão, fontes e estado → `EM_REVISAO` ou `QUARENTENA` |
| `EM_REVISAO` — correspondência editorial | responsável editorial | Markdown, PDF, hashes, acessibilidade e logo → `SUBMETIDO`, `CORRECOES` ou `BLOQUEADO` |
| `SUBMETIDO` — banca | banca nomeada | versão/hash, impedimentos e pareceres → `APROVADO`, `APROVADO_COM_EXIGENCIAS`, `CORRECOES` ou `REJEITADO` |
| `APROVADO_COM_EXIGENCIAS` — cumprimento | relator ou banca designada | matriz de exigências e nova versão/hash → `APROVADO` ou `CORRECOES` |
| `APROVADO` — homologação | autoridade humana competente | ata, pareceres, hashes, regularidade e acesso → `HOMOLOGADO`, `DEVOLVIDO` ou `SUSPENSO` |
| `HOMOLOGADO` — depósito interno | Biblioteca | pacote de integridade, ficha e classificação → `DEPOSITO_INTERNO` ou `BLOQUEADO` |
| `DEPOSITO_INTERNO` — publicação pública | Biblioteca e autoridade humana | sanitização, licença, metadados, links e rollback → `PUBLICADO`, `RESTRITO` ou `BLOQUEADO` |
| qualquer — correção pós-publicação | autoridade do ato e Biblioteca | errata, sucessor, novo hash e impacto → `CORRIGIDO`, `SUBSTITUIDO` ou `RETIRADO` |
| `QUARENTENA` — recuperação | Zeladoria ou guardião | origem, versão, classificação, erro e destino → `RECUPERADO` ou `MANTIDO` |
| `DESCARTE_ELEGIVEL` — resgate e descarte | Zeladoria e gate competente | prazo, sucessor, restauração, impedimentos e recibo → `RECLASSIFICADO`, `ARQUIVADO`, `DESCARTADO` ou `SUSPENSO` |

## Regras rápidas

1. Arquivo existente não equivale a aprovação.
2. Teste automatizado não equivale a banca ou homologação.
3. Manifestação de I.A. não substitui gate humano quando houver efeito humano ou externo.
4. Hash vincula parecer e decisão à versão examinada.
5. Alteração substantiva retorna ao gate afetado.
6. Publicação interna e pública são decisões diferentes.
7. Vencimento da quarentena gera elegibilidade, não exclusão automática.
