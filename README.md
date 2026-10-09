# Plugins Claude — Grupo IVM

Marketplace privado de plugins para o app Claude, com recortes **revisados** de projetos open source.

| Plugin | Origem | Conteúdo |
|---|---|---|
| `oh-my-claudecode` | [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) (MIT) | 12 skills de método + 19 agentes. Sem hooks, CLI `omc` ou MCP. |
| `supabase` | [supabase/agent-skills](https://github.com/supabase/agent-skills) (MIT) | Guia Supabase + 31 regras de Postgres |
| `vercel` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (MIT) | 9 skills (React/Next.js, deploy, otimização, design) |

O Chrome DevTools fica fora daqui: usa o marketplace oficial `ChromeDevTools/chrome-devtools-mcp`.

## Instalar no app

**Plugins → + Adicionar → Adicionar marketplace** → `VoIPMundoTelecom/claude-plugins`, com sincronização automática ligada.

## Como as atualizações chegam

1. Toda segunda, a Action **Sincronizar upstreams** puxa os repositórios originais e recorta de novo.
2. Se algo mudou, abre (ou atualiza) um PR `sync/upstream` com a varredura de segurança no corpo.
3. **Nada chega ao app sem você aprovar o merge.** Depois do merge, o app sincroniza sozinho.

Para rodar na hora: aba **Actions → Sincronizar upstreams → Run workflow**.

## Revisando um PR

- **Padrões de risco** (pipe para shell, `rm -rf`, `eval`, caminhos de credenciais, injeção de prompt): investigar qualquer ⚠️ novo.
- **⚙️ Código executável**: hoje só `deploy-to-vercel` e `vercel-optimize`. Arquivo novo nessa lista merece leitura.
- **🌐 Endpoints**: `deploy-to-vercel` envia o projeto para o endpoint de deploy "claimable" da Vercel. Endpoint novo, desconhecido ou fora dos domínios do fornecedor = não aprovar.

## Mudar o que entra

Edite `sources.json` (lista de skills por plugin) e rode:

```bash
python3 -I scripts/sync.py --repo-root .
python3 -I scripts/validate.py .
```

O script só copia `.md`, `.json`, `.txt` e código-fonte em texto; binários e arquivos compactados são descartados e listados na varredura.
