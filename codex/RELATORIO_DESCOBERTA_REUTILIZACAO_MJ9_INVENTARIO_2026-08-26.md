# Relatório de descoberta e implementação — MJ9

## Pedido atendido

`PED-CODEX-MJ9-INVENTARIO-2026-08-23-V2.0`, em estado preparado para triagem/não executado, e a Fase 0 de `PED-CODEX-UDF-CONSTITUINTE-2026-08-23-V1.0` foram convertidos em uma implementação local, offline e somente leitura nesta branch.

## Reutilização e limites

- A identidade, os estados documentais e o histórico da Casa permanecem fontes documentais; nenhum pedido original foi alterado.
- O inventário usa SHA-256, normalização, metadados sanitizados, duplicata exata por hash e duplicata provável por assinatura de nome/tamanho/MIME.
- O validador verifica manifesto, ausente/extra/hash divergente, identidade duplicada, declaração ausente, denominador e transições neutras.
- A referência observada de 310 arquivos/286 hashes únicos e 17 cópias idênticas do Juramento-Raiz continua um baseline histórico a reconciliar com fontes acessíveis; não é apresentada como medição desta execução local.
- Drive, GitHub, cofre, permissões, votação, promulgação, vigência automática, publicação e exclusão permanecem fora do pacote.

## Verificação

Os testes offline cobrem arquivo válido, inválido, incompleto/extra, duplicata, acentos, transição proibida, declaração/identidade, ZIP Slip e saída sem contagem/promulgação. O resultado de cada execução deve ser registrado junto ao commit e não substitui reconciliação humana das fontes.
