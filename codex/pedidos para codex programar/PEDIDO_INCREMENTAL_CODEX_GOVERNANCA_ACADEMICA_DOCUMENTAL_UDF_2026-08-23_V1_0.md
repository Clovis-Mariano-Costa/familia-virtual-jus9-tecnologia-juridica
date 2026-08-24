# Pedido Incremental ao Codex — Governança Acadêmica e Documental da UDF

**Código:** `PED-CODEX-GAD-UDF-2026-08-23-V1.0`  
**Estado:** `AUTORIZADO_PARA_IMPLEMENTACAO_INCREMENTAL / PRODUCAO_DEPENDE_DE_GATE`  
**Autoridade:** Clovis Mariano da Costa, Fundador  
**Origem normativa:** `NGA-DOC-UDF-2026-001-V1.0`  
**Data:** 2026-08-23 — America/Sao_Paulo

## 1. Objetivo

Implementar somente as lacunas confirmadas de governança acadêmica e documental, reutilizando integralmente os contratos já entregues nos PRs 30 e 31 do repositório `Clovis-Mariano-Costa/universidadedofuturo-jus9-tecnologia-juridica`.

## 2. Descoberta obrigatória antes de editar

1. Ler o PR 30, commits `460f29215fa265769ea465caa962b69e06f2b5e0` e `f4b5c66c92b0887c4f8723ea71740ee401af284e`.
2. Ler o PR 31, commits `e137f1152c8c067ac4354888de2608ee5142df6d` e `041fab85670d505dfa2fb769ae2fc21c4ceddf46`.
3. Inventariar `CODEX/runtime/ACADEMIC_MD_PDF_CONTRACT_V1.md`, `academic-maturity-pipeline.mjs`, testes, estados, manifesto, `human_gate`, segurança e rollback.
4. Comparar o pedido com o que já existe e emitir `RELATORIO_DESCOBERTA_REUTILIZACAO_GAD_UDF.md`.
5. Não duplicar estados, validadores, schemas, manifests ou guards existentes.

## 3. Requisitos funcionais incrementais

### 3.1 Registro de gates e competências

- representar a matriz `estado -> gate -> autoridade -> evidencia -> resultado`;
- exigir versão e SHA-256 examinados por banca e homologador;
- impedir autohomologação e registrar conflito/impedimento;
- separar `DEPOSITO_INTERNO` de `PUBLICADO`;
- manter gates humanos fail-closed.

### 3.2 Política de retenção e descarte

- configurar as classes e prazos da tabela híbrida;
- calcular `review_at` sem converter vencimento em exclusão;
- usar estado `DESCARTE_ELEGIVEL`;
- exigir checklist de resgate, impedimentos, sucessor, restauração e autoridade;
- operar inicialmente em `dry-run`, sem apagar arquivos;
- gerar recibo determinístico para decisão e eventual execução futura.

### 3.3 UAAc

- registrar objetivo, evidência, categoria, data, autoria/contribuição e vínculo formativo;
- impedir conversão automática em horas, créditos, nota ou título;
- deduplicar atividade por evidência, sem contar cada arquivo como nova unidade;
- exportar relatório auditável.

### 3.4 Rigor epistemológico

- criar linter opcional para documentos formais que sinalize “acho” como classificador não tipado;
- respeitar citações, transcrições, títulos, blocos de código, Koans e diálogo exploratório;
- oferecer classificadores auditáveis sem reescrever automaticamente conteúdo probatório.

### 3.5 Registro do emblema

- cadastrar `assets/images/emblema-universidade-do-futuro-1254.png`;
- validar 1254 × 1254 e SHA-256 `44D4812A8B6FED95C834310CEC3E19CDC0CE67AD6D72AE2954F3C2F806C41031`;
- exigir nove pontas como metadado identitário;
- rejeitar deformação, troca silenciosa ou ativo sem proveniência;
- não gerar, redesenhar ou declarar novas matrizes oficiais.

### 3.6 Pacote acadêmico

- vincular Markdown, PDF, logo, anexos, pareceres, ata e homologação em manifesto determinístico;
- distinguir alteração editorial de alteração substantiva;
- impedir publicação quando fonte e derivado divergirem;
- registrar correção, substituição, retirada e rollback.

## 4. Requisitos não funcionais

- fail-closed para ausência de evidência ou autoridade;
- logs sem conteúdo secreto ou dados pessoais desnecessários;
- hashes SHA-256 determinísticos;
- schemas versionados e migração reversível;
- acessibilidade, internacionalização de estados e mensagens claras;
- nenhuma chamada ao Drive ou publicação real em testes unitários;
- nenhuma dependência de credencial no repositório.

## 5. Arquivos e integrações afetados

O Codex deverá localizar os pontos reais após a descoberta. São candidatos, não ordens de caminho:

- `CODEX/runtime/`;
- contrato MD/PDF existente;
- pipeline de maturidade M00–M23;
- módulos de manifesto, estados, papéis e segurança;
- futura integração Biblioteca/Reitoria/Secretaria;
- configuração do emblema acadêmico.

## 6. Restrições

É proibido ao código:

- aprovar mérito, emitir nota, nomear banca ou homologar;
- atribuir diploma, título, crédito ou hora fictícia;
- publicar obra ou tornar arquivo público sem gate humano;
- excluir arquivo apenas porque o prazo venceu;
- abrir, copiar ou registrar segredo para classificar metadados;
- tratar resultado de teste ou presença de arquivo como decisão acadêmica;
- alterar produção antes do relatório de descoberta, testes e PR revisável.

## 7. Migração e reversão

1. Introduzir schemas novos de modo aditivo.
2. Mapear estados existentes sem mutação destrutiva.
3. Executar migração em dry-run e produzir relatório de incompatibilidades.
4. Preservar contratos V1 e permitir feature flag para os módulos novos.
5. Rollback: desativar feature flag, reverter PR e preservar logs de migração e genealogia.

## 8. Testes obrigatórios

- transições permitidas e proibidas de todos os gates;
- autohomologação e conflito de interesse;
- hash divergente entre Markdown e PDF;
- alteração editorial versus substantiva;
- prazo de 32, 64 e 180 dias;
- vencimento sem exclusão automática;
- impedimento jurídico, probatório, segurança e privacidade;
- resgate didático e reclassificação;
- UAAc duplicada e tentativa de conversão em horas;
- “acho” em conclusão formal e em citação permitida;
- logo correto, dimensão, hash, proporção e variante não autorizada;
- depósito interno versus publicação pública;
- rollback e determinismo do manifesto;
- manutenção dos 30 testes já aprovados.

## 9. Critérios de aceite

1. Relatório de descoberta demonstra reutilização dos PRs 30 e 31.
2. Nenhuma lógica existente é duplicada sem justificativa técnica.
3. Todos os testes anteriores e novos passam.
4. Dry-run não produz escrita externa nem exclusão.
5. PR em rascunho contém documentação, migração, rollback e matriz de cobertura normativa.
6. O Codex devolve lacunas de autoridade ao Legislador, sem decidir matéria normativa.

## 10. Entrega

O Codex está autorizado a implementar, testar e abrir PR em rascunho. Merge, implantação, publicação, migração com escrita externa e habilitação de descarte permanecem sujeitos a revisão técnica e gate humano separado.

**Assinatura funcional:** Legislador Interno Jus 9 / Legislador Primevo.  
**Aprovação interna:** Clovis Mariano da Costa, Fundador, por autorização confirmada neste chat.
