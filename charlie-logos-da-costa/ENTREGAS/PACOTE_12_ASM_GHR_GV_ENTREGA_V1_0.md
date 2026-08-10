# Pacote 12 — ASM, GHR e Gate Validator

Estado: IMPLEMENTADO_LOCALMENTE_E_TESTADO  
Escopo: Backend Acadêmico, Estados e Gates  
Classificação: INTERNO / IMPLEMENTAÇÃO / SEM SEGREDOS

## Arquivos

- `TRABALHOS/backend_academico/jus9_backend/models.py`
- `TRABALHOS/backend_academico/jus9_backend/asm.py`
- `TRABALHOS/backend_academico/jus9_backend/ghr.py`
- `TRABALHOS/backend_academico/jus9_backend/gates.py`
- `TRABALHOS/backend_academico/jus9_backend/store.py`
- `TRABALHOS/backend_academico/jus9_backend/api.py`
- `TRABALHOS/backend_academico/tests/test_backend.py`
- `TRABALHOS/backend_academico/README.md`

## Entregue

- ASM com estados M00–M23, transições explícitas, autoridade, evidência, versão, timestamp e rollback preservando eventos.
- GHR com JSON canônico, SHA-256, genealogia pai/filho, divergência de hash e tombstone de revogação.
- GV fail-closed para evidência ausente, segurança, isolamento, rollback, genealogia, sanitização, aprovação, homologação e publicação.
- Persistência JSON atômica para registros sanitizados.
- API Python local para registro, validação e transição.

## Testes

Comando:

```powershell
python -m unittest discover -s tests -v
```

Resultado: 8 testes aprovados.  
Verificação adicional: `python -m compileall -q jus9_backend tests` aprovado.

## Riscos e limites

- O pacote é uma implementação local mínima; não é deploy, merge ou publicação.
- Não inclui Biblioteca completa, CTPSV/CITAT, dicionários, frontend, titulação automática ou ensino automatizado.
- Persistência é JSON local; integração com banco, autenticação real e infraestrutura multi-tenant permanecem pendentes.
- O repositório já possuía alteração humana em `README_CASA_TRABALHO_V1.md`; ela não foi modificada.

## Pendências

- Revisão humana e revisão de segurança antes de qualquer merge.
- Integração com o contrato de proveniência/índice mestre e com o frontend.
- Testes E2E, concorrência, restauração real e execução em ambiente de integração.

## Próximo passo

Submeter este pacote à revisão humana, preservar o diff e só então preparar integração com Proveniência, Segurança e Integração E2E.
