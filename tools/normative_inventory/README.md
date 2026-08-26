# Inventário normativo MJ9 — modo somente leitura

Implementação local e determinística do pedido `PED-CODEX-MJ9-INVENTARIO-2026-08-23-V2.0` e da Fase 0 do pedido constituinte. A CLI recebe raízes locais já autorizadas e escreve somente em um diretório de saída explicitamente indicado.

```powershell
python -m tools.normative_inventory.cli --root .\charlie-logos-da-costa --output .\reports\inventory
```

O resultado contém JSON de inventário, matriz JSON/CSV, hashes SHA-256, estados neutros, relações, duplicatas exatas/prováveis e diferenças incrementais. O CSV neutraliza prefixos de fórmula. Sensíveis são apenas marcados; o conteúdo não é copiado para os relatórios.

Não há integração viva com Drive/GitHub, credenciais, escrita em fontes, exclusão, contagem de votos, promulgação ou publicação. Adaptadores externos devem fornecer metadados sanitizados e continuar sujeitos ao mesmo modo somente leitura. O rollback é remover os artefatos gerados e reverter o commit da branch; fontes e histórico permanecem intactos.
