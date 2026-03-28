# Requisitos — Pipeline RAG

## Requisito 1: Geração de embeddings
WHEN chunks de texto do GitHub forem recebidos para ingestão
THE SYSTEM SHALL gerar vetores de 384 dimensões usando o modelo HuggingFace `all-MiniLM-L6-v2`.

### Critérios de Aceitação
- [x] Dado um chunk de texto válido
- [x] Quando `embed()` for chamado
- [x] Então deve retornar um vetor de 384 floats
- [x] E o processamento em batch deve suportar listas de chunks
- [x] E usar padrão Singleton para evitar recarregar modelo

## Requisito 2: Armazenamento vetorial
WHEN embeddings forem gerados
THE SYSTEM SHALL armazená-los no ChromaDB com metadados (tipo, data, repositório, autor).

### Critérios de Aceitação
- [x] Dado um vetor + metadados
- [x] Quando `upsert()` for chamado
- [x] Então o vetor deve ser persistido na collection do ChromaDB
- [x] E upserts com mesmo ID devem atualizar (não duplicar)
- [x] E metadados devem incluir: tipo (commit/pr/issue), data, repositório, autor
- [x] E usar padrão Singleton para cliente ChromaDB

## Requisito 3: Ingestão automática
WHEN o horário do cron for atingido (2x/dia)
THE SYSTEM SHALL executar a pipeline completa: coletar dados → gerar chunks → embeddar → armazenar.

### Critérios de Aceitação
- [x] A ingestão roda como background task do FastAPI
- [x] Não bloqueia endpoints da API durante execução
- [x] Loga início, fim e quantidade de chunks processados

## Requisito 4: Busca semântica
WHEN o usuário enviar uma pergunta via POST /insights
THE SYSTEM SHALL embeddar a query e buscar os 5 chunks mais similares por cosine similarity.

### Critérios de Aceitação
- [x] Dado a pergunta "Quando sou mais produtivo?"
- [x] Quando a busca vetorial executar
- [x] Então deve retornar os 5 chunks com maior similaridade
- [x] E cada resultado deve incluir o texto do chunk e metadados

## Requisito 5: Geração de insight via LLM
WHEN os top-5 chunks forem recuperados
THE SYSTEM SHALL montar um prompt com contexto + pergunta e enviar ao LLM via aisuite.

### Critérios de Aceitação
- [x] O prompt deve incluir os chunks como contexto e a pergunta original
- [x] A resposta do LLM deve ser parseada em: resumo, evidência, recomendação
- [x] Deve funcionar com `ollama:llama3.1` (dev) e `openai:gpt-4o-mini` (prod)
- [x] Timeout configurado para 120s (modelos locais)
- [x] Parsing flexível para respostas JSON não-string

## Requisito 6: Endpoint de insights
WHEN o usuário enviar POST /insights com um campo `query`
THE SYSTEM SHALL retornar um JSON com o insight estruturado.

### Critérios de Aceitação
- [x] Request: `{"query": "Quando sou mais produtivo?"}`
- [x] Response: `{"summary": "...", "evidence": "...", "recommendation": "...", "sources": [...]}`
- [x] Retorna 400 se query estiver vazia
- [x] Retorna 503 se LLM não estiver disponível (com mensagem clara)

## Requisito 7: Modelo de resposta
WHEN um insight for gerado
THE SYSTEM SHALL estruturá-lo no modelo Insight com campos: resumo, evidência, recomendação e fontes.

### Critérios de Aceitação
- [x] `summary`: texto curto com a resposta principal
- [x] `evidence`: dados que sustentam a resposta
- [x] `recommendation`: sugestão acionável
- [x] `sources`: lista dos chunks usados como contexto

## Requisito 8: Status da ingestão
WHEN a ingestão estiver em execução
THE SYSTEM SHALL expor endpoint GET /ingest/status com progresso em tempo real.

### Critérios de Aceitação
- [x] Retorna: running, step, progress, total, logs
- [x] Frontend faz polling a cada 1s durante execução
- [x] Exibe painel com logs em tempo real

## Requisito 9: Ingestão manual
WHEN o usuário clicar em "Executar Ingestão" na página de Configurações
THE SYSTEM SHALL iniciar ingestão imediatamente em background.

### Critérios de Aceitação
- [x] POST /ingest inicia ingestão em background
- [x] Retorna imediatamente com status "started"
- [x] Botão desabilitado enquanto ingestão está rodando

## Requisito 10: Rate limiting
WHEN múltiplas requisições forem feitas aos endpoints
THE SYSTEM SHALL limitar a taxa de requisições por IP.

### Critérios de Aceitação
- [x] POST /insights: 10 requisições/minuto
- [x] GET /metrics: 30 requisições/minuto
- [x] POST /ingest: 5 requisições/hora
- [x] Retorna 429 quando limite excedido

## Requisito 11: Cache de métricas
WHEN métricas forem requisitadas
THE SYSTEM SHALL cachear resultados por 60 segundos.

### Critérios de Aceitação
- [x] Cache in-memory com TTL de 60s
- [x] Chave baseada em from_date e to_date
- [x] Reduz chamadas à API do GitHub

## Requisito 12: Health check detalhado
WHEN GET /health/detailed for requisitado
THE SYSTEM SHALL verificar status de todos os serviços.

### Critérios de Aceitação
- [x] Verifica: API, ChromaDB, GitHub, LLM (Ollama/OpenAI)
- [x] Retorna status individual de cada serviço
- [x] Status geral: "ok" ou "degraded"
