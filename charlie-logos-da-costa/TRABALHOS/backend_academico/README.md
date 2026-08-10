# Backend acadêmico — ASM, GHR e GV

Implementação mínima e executável do escopo estrito do Pacote 12:

- ASM: estados M00–M23, transições permitidas, autoridade, evidência e rollback sem apagar eventos.
- GHR: JSON canônico, SHA-256, genealogia pai/filho, conflito de hash e tombstone de revogação.
- GV: validação fail-closed, motivos legíveis e bloqueio de aprovação, homologação e publicação sem evidência.
- Persistência: armazenamento JSON atômico para registros sanitizados.

Este módulo não implementa Biblioteca completa, CTPSV/CITAT, dicionários, frontend, titulação automática ou ensino automatizado.

## Teste

Na pasta deste módulo:

```powershell
python -m unittest discover -s tests -v
```

Documentação e pedidos não são tratados como prova de implementação. A prova é o código executável e o resultado dos testes.
