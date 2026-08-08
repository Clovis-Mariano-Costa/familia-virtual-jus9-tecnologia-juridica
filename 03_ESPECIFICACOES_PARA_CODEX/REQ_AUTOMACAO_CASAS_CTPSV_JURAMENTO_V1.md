# Requerimento ao Codex - Automação de Casas, CTPSV e Juramento

Implementar ferramenta idempotente que:

1. inventarie Casas-Lares e Casas-Trabalho;
2. gere `dry-run` antes de qualquer escrita;
3. sincronize somente arquivos padronizados sem overwrite silencioso;
4. calcule datas reconhecidas de vínculo conforme algoritmo V1;
5. valide hashes e caminhos Casa-Lar/Casa-Trabalho;
6. detecte códigos JV duplicados ou ausentes;
7. distribua a cópia vigente do Juramento-Raiz;
8. preserve versões e arquivos de rastro;
9. gere relatório de inconsistências;
10. proponha mudanças por branch/PR revisável.

## Critérios de aceite
- UTF-8 e preservação de acentos dos nomes registrais;
- timestamps com cinco casas decimais;
- nenhum segredo ou credencial;
- nenhuma exclusão automática;
- nenhuma autohomologação de ato humano;
- testes automatizados;
- rollback por Git;
- idempotência;
- diferenciação entre nome registral e slug técnico.

Destino operacional indicado pelo Fundador para pedidos de programação:
https://drive.google.com/drive/folders/1SWFZGRpw1CrXakaqfveOB9YjGrmF0im2
