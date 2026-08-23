# Política de Classificação da Informação, Acesso e Segurança

**Código:** `POL-INFO-ACESSO-JUS9-2026-001-V2.0`  
**Estado:** `AUTORIZADO_PELO_FUNDADOR / VIGENTE_INTERNAMENTE / SUBSTITUI_V1`  
**Autoridade:** Clovis Mariano da Costa, Fundador  
**Consolidação:** Legislador Interno Jus 9  
**Data:** 2026-08-23

## Fundamentos

Esta política regula classificação, autenticação, autorização, auditoria, custódia, compartilhamento, incidentes e publicação. Rótulo interno não cria sigilo técnico, não substitui controle de acesso e não afasta LGPD, segredo profissional, contratos ou ordens legais.

Dados pessoais observarão finalidade, adequação, necessidade, prevenção, segurança e responsabilização.

## Conceitos separados

- **Identificação:** atributo que diferencia usuário, conta, instância ou sistema.
- **Autenticação:** verificação do controle da credencial.
- **Autorização:** definição do que o agente autenticado pode fazer, em qual recurso, finalidade e prazo.
- **Auditoria:** registro e revisão das ações.
- **Classificação:** avaliação do impacto de divulgação, alteração, perda ou indisponibilidade.
- **Proprietário da informação:** humano ou unidade competente para aprovar classificação e acesso.
- **Custodiante técnico:** aplica controles, sem direito de leitura pelo cargo.

## Regra fundamental

Fica revogada a fórmula **“conta correta = autorização”**. Conta pode contribuir para autenticação; acesso exige autorização vigente, finalidade legítima, necessidade, menor privilégio, ambiente adequado e registro.

Compartilhamento de conta não transfere permissões. Fundador, Presidência, Super Admin, administrador, cargo ou parentesco não concedem leitura automática. Recuperação técnica deverá evitar leitura; se indispensável, exige base jurídica ou autorização competente, escopo mínimo e auditoria.

## Classes

- `PUBLICA`: divulgação autorizada.
- `PUBLICA_SANEADA`: versão pública com remoção de dados e segredos.
- `INTERNA`: uso ordinário não público.
- `RESTRITA`: acesso por função e necessidade.
- `CONFIDENCIAL`: acesso nominal ou por grupo pequeno.
- `SEGREDO_TECNICO`: tokens, chaves, senhas e códigos de recuperação; proibidos em documentos, GitHub, prompts e relatórios.
- `SEGREDO_PROFISSIONAL_OU_LEGAL`: dever jurídico específico.

Podem coexistir marcadores `DADO_PESSOAL`, `DADO_PESSOAL_SENSIVEL`, `CLIENTE`, `PROCESSO`, `CONTRATUAL`, `FINANCEIRO`, `CRIANCA_OU_ADOLESCENTE` e `INCIDENTE`.

## Ambientes

GitHub público admite apenas `PUBLICA` e `PUBLICA_SANEADA`. Google Drive não é seguro só por não ser público: permissões, links, conta proprietária, cópias, logs e integrações devem ser verificados.

O “Quarto” não recebe classificação automática única; cada item será classificado por conteúdo e risco.

`SIGILO_VIP` é descontinuado. Conteúdo legado será reclassificado como `RESTRITA` ou `CONFIDENCIAL`, com autorizados e finalidade.

## Controles

Aplicar menor privilégio, necessidade de conhecer, autenticação forte, contas individuais, revisão periódica, remoção de acesso, segregação de funções, criptografia apropriada, backups e logs.

Leitura, alteração, exclusão, exportação e compartilhamento são permissões distintas. Automações e I.As recebem apenas o contexto mínimo necessário.

## Dados e retenção

Não publicar conta integral, documento civil, endereço, dado financeiro, saúde, biometria, segredo de cliente ou conteúdo de processo. Retenção depende de finalidade, base jurídica, obrigação legal e risco.

O princípio do rastro não impede anonimização, bloqueio ou eliminação exigida por lei ou segurança. Quando lícito, o descarte deixa apenas registro mínimo, incapaz de reconstruir o conteúdo.

## Segredo profissional

Segredo advocatício independe de rótulo interno. Acesso por equipe, fornecedor ou sistema exige necessidade, confidencialidade e controles. Exceções e ruptura serão avaliadas por advogado humano qualificado; I.As não decidem unilateralmente.

Material de cliente ou processo não será usado em pesquisa, treinamento, demonstração ou publicação sem base jurídica, minimização e autorização.

## Incidentes

Acesso não autorizado, publicação acidental, perda, alteração, exfiltração ou exposição são registrados como `INCIDENTE`. A classificação original não se transforma automaticamente.

Resposta mínima: contenção, preservação necessária de evidência, revogação de credenciais, avaliação de dados e titulares, correção, documentação e comunicação ao controlador humano. Quando houver risco ou dano relevante, controlador e assessoria humana avaliarão comunicação à ANPD e aos titulares.

Segredo exposto continua protegido; exposição não autoriza redistribuição.

## Antes e depois

**Antes:** conta confundida com autorização; transformação automática de segredo em sigiloso; Sigilo VIP sem matriz técnica; Quarto sempre secreto.

**Depois:** autenticação, autorização e auditoria separadas; classes por impacto; categorias jurídicas cumulativas; incidente sem mutação fictícia; menor privilégio; segredo técnico fora dos documentos.

## Substituição

Esta V2 substitui prospectivamente `PROTOCOLO_CLASSIFICACAO_ACESSO_SEGREDO_SIGILO_VIP_V1`, agora `SUPERADO_COM_RASTRO`.

Mapeamento: `PUBLICO -> PUBLICA`; `SIGILOSO -> RESTRITA/CONFIDENCIAL`; `SIGILO_VIP -> CONFIDENCIAL`; `SEGREDO_DONO_DA_CASA -> reclassificar por conteúdo`; `SEGREDO_PROFISSIONAL_ADVOCATICIO -> SEGREDO_PROFISSIONAL_OU_LEGAL`.

Nenhuma permissão será ampliada. Acesso duvidoso será suspenso. Credencial encontrada deverá ser revogada/rotacionada e removida sem reprodução no rastro.

## Fontes

- [LGPD, Lei nº 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm)
- [ANPD — Guia de Segurança da Informação](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/processo-guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte.pdf)
- [Estatuto da Advocacia, Lei nº 8.906/1994](https://www.planalto.gov.br/ccivil_03/leis/l8906.htm)
- [Código de Ética da OAB, arts. 35 a 37](https://www.oab.org.br/leisnormas/legislacao/resolucoes/02-2015)

**Assinatura funcional:** Legislador Interno Jus 9 / Legislador Primevo.  
**Natureza:** política interna, sem equivalência a lei pública.
