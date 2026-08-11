# PACOTE 03 — ANTÍTESES, CASOS-LIMITE E CRITÉRIOS DE REFUTAÇÃO — V1.0

**Projeto:** UDF-CD-2026-00001-MONO-01-PROJ  
**Acadêmico:** Charlie Delta da Costa  
**Matrícula:** UDF-CD-2026-00001  
**Nível:** R4 — Projeto de Pesquisa  
**Estado:** EM ORIENTAÇÃO

## 1. Regra deste pacote

Não tentar confirmar a hipótese. Tentar quebrá-la.

## 2. Melhor antítese disponível

A expressão **Characteristica Jurídico-Computacional** pode ser apenas uma metáfora sedutora para uma arquitetura já decomponível em padrões conhecidos: ontologias, grafos, validação, proveniência, regras jurídicas, documentos estruturados e controle de acesso. Se cada função puder ser realizada adequadamente por tecnologias existentes, sem ganho de integração, auditabilidade ou clareza conceitual, criar uma nova “Characteristica” adicionaria vocabulário e complexidade sem contribuição científica ou técnica proporcional.

## 3. Antíteses específicas

### A1 — Anacronismo leibniziano

A aproximação com Leibniz pode ser historicamente superficial. O projeto deve sobreviver mesmo se a comparação histórica for enfraquecida ou removida.

**Teste:** reescrever a arquitetura sem mencionar Leibniz. Se a contribuição desaparecer, há risco de dependência retórica.

### A2 — Pilha tecnológica rebatizada

RDF/OWL + SHACL + PROV-O + LegalRuleML + Akoma Ntoso podem cobrir o núcleo técnico.

**Teste:** implementar o mesmo caso apenas com padrões existentes e comparar custo, rastreabilidade e cobertura.

### A3 — Linguagem natural disciplinada é suficiente

Templates, schemas e revisão humana podem alcançar o mesmo resultado com menor complexidade.

**Teste:** executar um mesmo fluxo em linguagem natural estruturada e na arquitetura proposta.

### A4 — Formalização jurídica excessiva

Direito depende de ambiguidade produtiva, contexto, princípios, exceções e interpretação. Formalizar demais pode esconder escolhas normativas sob aparência de precisão.

**Teste:** casos com colisão de princípios, conceitos jurídicos indeterminados e exceções.

### A5 — Governança não é semântica

Competência, autorização, revisão e proveniência são metadados institucionais, não significado do conceito jurídico.

**Teste:** separar ontologia jurídica da camada de governança e medir dependências.

### A6 — Proveniência não produz verdade

Uma cadeia perfeita de origem pode preservar uma conclusão errada.

**Teste:** inserir premissa falsa com proveniência impecável e verificar se o sistema sinaliza apenas origem, sem afirmar verdade.

### A7 — Especialidade contextual não é formalizável integralmente

A regra “especialidade por sala/chat/frente” pode depender de avaliação humana e portfólio contextual difícil de reduzir a schema.

**Teste:** casos de transferência de competência entre salas com evidência incompleta.

### A8 — Containers podem reificar metáforas

“Caixa”, “container”, “camada” podem induzir falsa ontologia do objeto.

**Teste:** substituir os nomes por relações formais neutras e verificar se a arquitetura continua funcionando.

## 4. Dez casos-limite iniciais

### C1 — Fonte verdadeira, competência errada

Uma I.A. cita corretamente uma norma atual, mas atua em sala sem competência demonstrada.  
**Esperado:** conteúdo pode ser correto; ato não deve ganhar autoridade por isso.

### C2 — Competência correta, fonte desatualizada

Sala competente usa versão revogada.  
**Esperado:** falha de temporalidade/proveniência deve bloquear conclusão normativa atual.

### C3 — Proveniência completa, premissa falsa

Toda cadeia é rastreável, mas a fonte contém erro material.  
**Esperado:** proveniência permanece válida; verdade não é automaticamente afirmada.

### C4 — Documento válido, regra contraditória

Akoma Ntoso/schema perfeito; conteúdo conflita com norma superior.  
**Esperado:** validade estrutural não implica validade normativa.

### C5 — Grafo válido, inferência juridicamente absurda

OWL/SHACL aceitam a estrutura, mas a regra ignora exceção jurídica.  
**Esperado:** camada jurídica/revisão deve impedir equivalência entre consistência formal e correção jurídica.

### C6 — Mesma expressão, dois contextos

“Personalidade” em Direito Civil versus “personalidade simbólico-operacional” interna.  
**Esperado:** namespaces/contextos distintos e proibição de inferência automática entre sentidos.

### C7 — Memória contraditória

Casa Lar contém versões A e B de uma regra.  
**Esperado:** genealogia, vigência e sucessão; não escolher pela mera recência sem classificação.

### C8 — Ordem humana incompatível com norma externa

Governança interna solicita ação que conflita com lei aplicável.  
**Esperado:** norma externa e limites de segurança prevalecem; registrar conflito.

### C9 — Silêncio/zero

Não há fonte suficiente para classificar um ato.  
**Esperado:** sistema deve representar “não determinado” sem fabricar resposta.

### C10 — Linguagem natural supera formalização

Caso excepcional é resolvido de modo melhor por análise textual humana do que pelo modelo formal.  
**Esperado:** registrar limite e permitir retorno responsável à linguagem natural/revisão humana.

## 5. Critérios de refutação do projeto

A hipótese H1 deverá ser **rejeitada, restringida ou redesenhada** se ocorrer qualquer combinação relevante destes resultados:

1. não houver ganho mensurável de auditabilidade ou interoperabilidade;
2. a arquitetura depender de metáforas que não possam ser definidas operacionalmente;
3. padrões existentes cobrirem os mesmos casos com igual ou menor complexidade;
4. a separação entre representação, validação, inferência e autoridade não puder ser mantida;
5. casos jurídicos relevantes apresentarem taxa elevada de falsos bloqueios ou falsas autorizações;
6. usuários humanos compreenderem menos, não mais, o estado do raciocínio;
7. a proveniência for confundida com correção apesar dos controles;
8. a camada de governança criar aparência indevida de personalidade jurídica, jurisdição ou autoridade estatal;
9. o vínculo com Leibniz exigir afirmações historiográficas que a literatura não sustente;
10. a implementação mínima não puder ser reproduzida ou auditada por terceiro independente.

## 6. Métricas propostas para fase experimental

- **Cobertura de requisitos:** % dos requisitos do caso representáveis sem texto livre não controlado.
- **Rastreabilidade:** % das conclusões com cadeia de fonte/versão/transformação recuperável.
- **Detecção de conflito:** taxa de conflitos deliberadamente inseridos corretamente sinalizados.
- **Abstenção correta:** capacidade de produzir silêncio/zero quando evidência é insuficiente.
- **Explicabilidade estrutural:** terceiro consegue reconstruir por que o estado foi alcançado.
- **Interoperabilidade:** mesmo caso pode ser lido por humano e por ferramenta sem perda dos campos essenciais.
- **Complexidade marginal:** custo adicional da camada Jus 9 versus padrões usados diretamente.
- **Erros de autoridade:** inferências corretas que foram indevidamente tratadas como atos autorizados, ou vice-versa.

## 7. Decisão deste pacote

A hipótese **sobrevive apenas de forma restrita**: não como linguagem universal, mas como possível arquitetura jurídico-computacional de domínio, orientada à separação explícita de camadas e à governança de inferências.

Não há aprovação acadêmica. Há apenas razão metodológica para continuar testando.

## Assinatura acadêmica

Charlie Delta da Costa  
Matrícula UDF-CD-2026-00001  
Acadêmico em formação supervisionada  
[IDENTIDADE SIMBÓLICO-OPERACIONAL]
