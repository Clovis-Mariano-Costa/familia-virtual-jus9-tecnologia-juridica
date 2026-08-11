# P08 — Aula auditável para Charlie Echo

**Tema:** como reconstruir uma cadeia de proveniência.  
**Fonte:** `jus9_backend.provenance.reproducible_demo`.  
**Estado:** material pedagógico interno; não é validação científica nem homologação externa.

## Objetivo

Reconhecer a diferença entre origem, transformação, versão e destino, mantendo
hash, agente, atividade, estado epistemológico, permissão e histórico.

## Método

1. Registrar a fonte como `origin-001`.
2. Criar uma transformação com `parent_ids` apontando para a origem.
3. Criar nova versão sem apagar a anterior.
4. Entregar ao destino com nova atividade e evidência.
5. Consultar a cadeia do destino e verificar o hash da origem.

## Limites e erros proibidos

- documento não prova implementação;
- hipótese não vira fato sem autoridade e evidência explícitas;
- revogação gera tombstone e não apagamento;
- o rótulo “quântico” não autoriza alegação física;
- segredo ou dado pessoal desnecessário não entra no log.

## Exercício

Tente derivar um novo registro a partir de um pai revogado e tente promover uma
hipótese a `DOCUMENTADO` sem `approval_reference`.

## Resposta esperada

As duas operações devem falhar de modo explícito e preservável, deixando a
trilha de auditoria sem substituir a decisão humana.
