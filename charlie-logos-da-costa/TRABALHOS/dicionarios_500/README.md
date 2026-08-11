# Pipeline de Dicionários — 500 Verbetes

Implementação executável do eixo `JUS9 CODEX | Dicionários e 500 Verbetes`.

## Escopo

- corpus estruturado de 500 sementes não canônicas;
- contrato mínimo por entrada;
- validação de estados, fontes e campos obrigatórios;
- duplicidade exata normalizada;
- genealogia sem apagamento;
- gate de promoção fail-closed;
- consulta web por termo e estado;
- pacote pedagógico sanitizado para Charlie Echo.

O corpus não canoniza entradas. A presença de uma entrada no JSON ou na página não equivale a fonte verificada, revisão independente ou aprovação humana.

## Execução

Na pasta `TRABALHOS/dicionarios_500`:

```powershell
python validate_corpus.py
python -m unittest discover -s tests -v
```

O validador retorna sucesso para um corpus de sementes estruturalmente íntegro e informa campos ainda ausentes. Retorna falha quando houver estado inválido, identificador duplicado, fonte malformada ou promoção canônica sem evidência.

## Estado

`SEMENTE_NAO_CANONICO / AGUARDA_REVALIDACAO_V2_0`

Fonte declarada: lote de 500 do Dicionário da Universidade do Futuro, versão V3, fila `PACOTE_03_FILA_REVISAO_DICIONARIO_500_SEMENTES_NAO_CANONICAS_V1_0`.
