# PACOTE 02 — ESTADO DA ARTE EXTERNO E MATRIZ DE FONTES — V1.0

**Projeto:** UDF-CD-2026-00001-MONO-01-PROJ  
**Acadêmico:** Charlie Delta da Costa  
**Matrícula:** UDF-CD-2026-00001  
**Nível:** R4 — Projeto de Pesquisa  
**Estado:** EM ORIENTAÇÃO  
**Data de pesquisa:** 10 de agosto de 2026

## 1. Pergunta desta espira

Quais partes do problema da **Characteristica Jurídico-Computacional** já são tratadas por tradições filosóficas, linguagens formais e padrões técnicos existentes, e qual lacuna específica ainda justificaria a pesquisa?

## 2. Leibniz: ponto de partida histórico, não selo de legitimidade

A literatura histórica consultada sustenta como ponto seguro que a *Dissertatio de Arte Combinatoria* (1666) já esboçava um plano de característica universal e cálculo lógico. A pesquisa contemporânea também adverte que **characteristica universalis** e **calculus ratiocinator** não devem ser tratados como duas caixas históricas absolutamente nítidas: a distinção terminológica/conceitual é objeto de debate.

### Consequência metodológica

Esta monografia **não** afirmará:

- que RDF, OWL, LegalRuleML ou qualquer tecnologia atual “realiza” Leibniz;
- que a Jus 9 Tecnologia Jurídica completou a *Characteristica Universalis*;
- que “Characteristica Jurídico-Computacional” é uma identidade histórica com a proposta leibniziana.

Ela testará apenas uma **hipótese comparativa e arquitetural**: se alguns problemas leibnizianos de representação, composição e operação racional reaparecem, com limites de domínio explícitos, na construção de uma linguagem jurídico-computacional governada.

## 3. Estado da arte técnico: decomposição funcional

### 3.1 RDF — representação em grafo

RDF fornece um modelo abstrato para representar recursos e relações em grafos. A versão RDF 1.2 encontrava-se, em 2026, em trilha de padronização no W3C, enquanto RDF 1.1 permanecia a Recommendation estável indicada pela própria especificação.

**Contribuição ao projeto:** relações identificáveis e interoperáveis.  
**Não resolve sozinho:** semântica jurídica normativa, validação de domínio, proveniência suficiente, autoridade ou decisão.

### 3.2 OWL 2 — ontologias e semântica formal

OWL 2 permite definir ontologias com classes, propriedades, indivíduos e semântica formal.

**Contribuição:** vocabulários formais, taxonomias, relações e inferências sob semânticas especificadas.  
**Limite:** mundo jurídico inclui exceções, defeasibilidade, temporalidade, autoridade, versões e conflitos que não se reduzem automaticamente a ontologia descritiva.

### 3.3 SHACL — restrições e validação

SHACL descreve e valida grafos RDF por meio de *shapes*. Em 2026, o W3C também mantinha trabalho de SHACL 1.2, inclusive uma trilha de regras em Working Draft.

**Contribuição:** declarar condições mínimas para que um objeto seja considerado estruturalmente válido.  
**Analogia útil:** possível camada técnica para “portões” e requisitos de containers.  
**Cuidado:** validação estrutural não equivale a validade jurídica.

### 3.4 PROV-O — proveniência

PROV-O é uma Recommendation do W3C para intercâmbio interoperável de informação de proveniência usando OWL/RDF.

**Contribuição:** representar entidades, atividades, agentes e relações de derivação/atribuição.  
**Relevância interna:** aproxima-se do problema do Elefante Colorido quanto à necessidade de demonstrar de onde veio um registro e por quais transformações passou.  
**Limite:** proveniência não prova verdade material nem legitimidade do conteúdo.

### 3.5 Akoma Ntoso — documentos jurídicos estruturados

Akoma Ntoso é padrão OASIS para estruturação de documentos parlamentares, legislativos e judiciais.

**Contribuição:** estrutura documental, identificação de partes, referências e elementos jurídicos.  
**Limite:** modelar documento jurídico não é o mesmo que modelar raciocínio, competência, inferência ou memória de uma I.A.

### 3.6 LegalRuleML — regras e normas jurídicas

LegalRuleML oferece uma linguagem para representar regras jurídicas e aspectos normativos em formato estruturado.

**Contribuição:** normas, regras, qualificações e relações jurídico-lógicas.  
**Limite:** não substitui interpretação humana, governança, prova, contexto institucional nem controle de autoridade.

## 4. Matriz preliminar de correspondência

| Problema | Leibniz como antecedente investigativo | Tecnologia contemporânea | Elemento Jus 9 em teste | Risco |
|---|---|---|---|---|
| vocabulário | característica / signos | RDF, OWL | Dicionário Canônico | universalismo indevido |
| composição | arte combinatória | RDF/OWL | caixas, containers, relações | metáfora sem semântica |
| inferência | cálculo racional | OWL reasoners, regras, SHACL Rules, LegalRuleML | verbo–ato, portões, adjudicação experimental | automatizar interpretação indevidamente |
| validade estrutural | cálculo verificável | SHACL | gates / requisitos | confundir conformidade com validade jurídica |
| proveniência | demonstração/encadeamento racional | PROV-O | Elefante Colorido | confundir origem com verdade |
| documento jurídico | — | Akoma Ntoso | atos, protocolos, normas | estruturar texto sem compreender norma |
| regra jurídica | — | LegalRuleML | normas internas / especialidades | descontextualização normativa |
| memória | enciclopédia / ciência geral como antecedente de pesquisa | provenance + KGs + stores | Casa Lar, Casa Trabalho, Elefante | memória não é conhecimento verdadeiro |
| governança | não equivalente histórico | políticas, avaliação, controle de acesso | competência, reitoria, especialidade por sala | antropomorfização / autoridade fictícia |

## 5. Lacuna de pesquisa proposta

Nenhum padrão analisado, isoladamente, cobre o conjunto simultâneo:

1. vocabulário jurídico controlado;
2. relações semânticas;
3. estrutura normativa;
4. regras e inferência;
5. validade estrutural;
6. proveniência;
7. versionamento e memória;
8. autoridade/competência;
9. contraditório/revisão;
10. separação explícita entre estado simbólico-institucional interno e efeitos jurídicos externos.

A contribuição potencial da monografia não será criar “uma nova linguagem universal”, mas **especificar e testar uma arquitetura de integração limitada ao domínio da Jus 9 Tecnologia Jurídica e ao laboratório jurídico-computacional**, reutilizando padrões existentes onde forem suficientes e criando apenas as camadas de governança ou composição que a evidência demonstrar necessárias.

## 6. Hipótese refinada H1

> Uma Characteristica Jurídico-Computacional de domínio pode ser modelada como arquitetura em camadas que separa vocabulário, representação, validação, proveniência, regra, autoridade, memória e revisão, permitindo interoperabilidade humano–I.A. e I.A.–I.A. mais auditável do que documentos em linguagem natural desacompanhados dessas camadas.

## 7. Hipótese nula H0

> A combinação proposta não produz ganho explicativo, operacional ou de auditabilidade suficiente em relação ao uso disciplinado de padrões e documentos já existentes; “Characteristica Jurídico-Computacional” seria apenas um novo nome para uma pilha tecnológica conhecida.

## 8. Fontes externas mínimas registradas

### Historiografia e filosofia

- Stanford Encyclopedia of Philosophy — **Gottfried Wilhelm Leibniz**: https://plato.stanford.edu/entries/leibniz/
- Esquisabel, Oscar M. — **Lenguaje racional universal versus “calculus ratiocinator”. ¿Se aplica esta distinción a Leibniz?**: https://ri.conicet.gov.ar/handle/11336/106746
- Research literature on *lingua characterica* / *calculus ratiocinator* — Review of Symbolic Logic, DOI 10.1017/S175502031900025X.

### Padrões técnicos primários

- W3C — RDF 1.2 Concepts: https://www.w3.org/TR/rdf12-concepts/
- W3C — OWL 2 Overview: https://www.w3.org/TR/owl2-overview/
- W3C — SHACL: https://www.w3.org/TR/shacl/
- W3C — SHACL 1.2 Core: https://www.w3.org/TR/shacl12-core/
- W3C — PROV-O: https://www.w3.org/TR/prov-o/
- OASIS — LegalRuleML 1.0: https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/
- OASIS — Akoma Ntoso 1.0: https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html

## 9. Classificação de evidência

- **História de Leibniz:** sustentação bibliográfica; ainda requer leitura ampliada de textos primários antes da monografia.
- **Padrões W3C/OASIS:** fontes primárias normativas/técnicas.
- **Correspondências com Jus 9:** hipóteses analíticas internas, não fatos históricos.
- **Lacuna:** hipótese de pesquisa a ser testada por comparação e protótipo mínimo; não descoberta confirmada.

## 10. Saída do pacote

**Resultado:** há justificativa provisória para prosseguir, desde que o projeto abandone qualquer pretensão universalista forte e trate a Characteristica Jurídico-Computacional como **linguagem/arquitetura de domínio governada e falsificável**.

**Próximo pacote:** contraditório, antíteses, casos-limite e critérios de refutação.

## Assinatura acadêmica

Charlie Delta da Costa  
Matrícula UDF-CD-2026-00001  
Acadêmico em formação supervisionada  
[IDENTIDADE SIMBÓLICO-OPERACIONAL]
