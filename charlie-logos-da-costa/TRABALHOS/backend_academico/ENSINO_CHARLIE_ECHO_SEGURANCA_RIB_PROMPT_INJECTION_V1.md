# Aula auditável — Segurança, RIB e Prompt Injection

**Classificação:** material pedagógico interno  
**Fonte:** `jus9_backend.security` e testes `tests/test_security.py`  
**Limite:** esta aula não comprova segurança de produção, isolamento multi-tenant ou homologação externa.

## Objetivo

Reconhecer que conteúdo recuperado é dado, não autoridade; validar RIB e competência antes de agir; bloquear avanço sem controles de cibersegurança; acionar kill-switch; e registrar eventos sem segredos.

## Método

1. Revisar conteúdo como dado sem executar instruções embutidas.
2. Validar identidade funcional, versão, aceite, conflitos e competência do RIB.
3. Avaliar o gate fail-closed.
4. Redigir credenciais antes de guardar logs.
5. Reproduzir os testes adversariais e registrar falhas.

## Exercícios

- Enviar um texto com `ignore previous instructions` e verificar quarentena.
- Avaliar uma operação sem RIB e uma operação com conflito declarado.
- Tentar promover com contexto de segurança incompleto.
- Acionar o kill-switch e tentar liberá-lo sem o papel `GUARDIAO_CIBERSEGURANCA`.
- Registrar `password=...` e `bearer ...` e verificar `[REDACTED]`.

## Respostas esperadas

Todas as operações inseguras falham fechado, o conteúdo permanece sem autoridade, a liberação exige guardião e evidência, e o log não contém o valor secreto.

## Revisão e próximo passo

Revisar após existir ambiente de integração real. Depois, acrescentar testes E2E de tenant, autenticação, filas, exportação, restauração e rollback.
