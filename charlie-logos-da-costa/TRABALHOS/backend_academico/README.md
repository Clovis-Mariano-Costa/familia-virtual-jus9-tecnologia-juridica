# Backend acadêmico — ASM, GHR e GV

Implementação mínima e executável do escopo estrito do Pacote 12:

- ASM: estados M00–M23, transições permitidas, autoridade, evidência e rollback sem apagar eventos.
- GHR: JSON canônico, SHA-256, genealogia pai/filho, conflito de hash e tombstone de revogação.
- Proveniência: `ProvenanceRecord`, estados epistemológicos, cadeia reproduzível, índice, auditoria append-only, revogação e tombstone.
- GV: validação fail-closed, motivos legíveis e bloqueio de aprovação, homologação e publicação sem evidência.
- Segurança: RIB mínimo, conteúdo não confiável sem autoridade, quarentena de prompt injection, gate de cibersegurança fail-closed, kill-switch e logs sanitizados.
- Persistência: armazenamento JSON atômico para registros sanitizados.

Este módulo não implementa Biblioteca completa, CTPSV/CITAT, dicionários, frontend, titulação automática ou ensino automatizado.

O registro de proveniência não promove hipótese a fato automaticamente, não remove histórico e não interpreta o campo “quântico” como alegação física.

## Teste

Na pasta deste módulo:

```powershell
python -m unittest discover -s tests -v
```

Documentação e pedidos não são tratados como prova de implementação. A prova é o código executável e o resultado dos testes. A camada de segurança é deliberadamente mínima e ainda não substitui integração E2E, isolamento multi-tenant real ou revisão humana.
