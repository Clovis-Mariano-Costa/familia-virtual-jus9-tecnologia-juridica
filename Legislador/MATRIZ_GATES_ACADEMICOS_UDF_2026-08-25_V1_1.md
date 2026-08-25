# Matriz Operacional de Gates Acadêmicos da Universidade do Futuro

**Código:** `MAT-GATE-UDF-2026-08-25-V1.1`  
**Norma de origem:** `NGA-DOC-UDF-2026-001-V1.1`  
**Estado:** `VIGENTE_TRANSITORIAMENTE`  

| Entrada e gate | Responsável | Evidência mínima | Resultado permitido |
|---|---|---|---|
| `RASCUNHO` — aceitação da fonte | autor e orientador | fonte, autoria, versão, proveniência e estado | `EM_REVISAO` ou `QUARENTENA` |
| `EM_REVISAO` — correspondência editorial | responsável editorial | fonte, PDF, hashes, acessibilidade e emblema | `SUBMETIDO`, `CORRECOES` ou `BLOQUEADO` |
| `SUBMETIDO` — banca | banca nomeada | versão/hash, qualificações, impedimentos, pareceres | `APROVADO`, `APROVADO_COM_EXIGENCIAS`, `CORRECOES`, `BLOQUEADO` ou `REJEITADO` |
| `APROVADO_COM_EXIGENCIAS` — cumprimento | relator ou banca | matriz de exigências e nova versão/hash | `APROVADO` ou `CORRECOES` |
| `APROVADO` — homologação | autoridade humana competente | ata, pareceres, hashes, regularidade e acesso | `HOMOLOGADO`, `DEVOLVIDO` ou `SUSPENSO` |
| `HOMOLOGADO` — depósito interno | Biblioteca | pacote de integridade, ficha e classificação | `DEPOSITO_INTERNO` ou `BLOQUEADO` |
| `DEPOSITO_INTERNO` — publicação pública | Biblioteca e autoridade humana | sanitização, licença, metadados, links e rollback | `PUBLICADO`, `RESTRITO` ou `BLOQUEADO` |
| qualquer — correção pós-publicação | autoridade do ato e Biblioteca | errata, sucessor, novo hash e impacto | `CORRIGIDO`, `SUBSTITUIDO`, `RETIRADO` ou `RESTRITO` |
| `QUARENTENA` — recuperação | Zeladoria ou guardião | origem, versão, classificação, erro e destino | `RECUPERADO` ou `MANTIDO` |
| `DESCARTE_ELEGIVEL` — resgate e descarte | Zeladoria e gate competente | prazo, sucessor, restauração, impedimentos e recibo | `RECLASSIFICADO`, `ARQUIVADO`, `DESCARTADO` ou `SUSPENSO` |

## Regras de bloqueio

1. Arquivo existente não equivale a aprovação.
2. Teste automatizado não equivale a banca ou homologação.
3. Manifestação de I.A. não substitui gate humano quando houver efeito humano ou externo.
4. Hash vincula parecer e decisão à versão examinada.
5. Alteração substantiva retorna ao gate material afetado.
6. Publicação interna e pública são decisões diferentes.
7. Vencimento da quarentena gera elegibilidade, não exclusão automática.
8. Autohomologação, conflito não tratado, hash divergente ou ausência de autoridade bloqueiam o avanço.

