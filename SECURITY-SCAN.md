# Varredura de segurança

Gerada por `scripts/sync.py`. Revise antes de aprovar o PR.

## oh-my-claudecode

Upstream: `https://github.com/Yeachan-Heo/oh-my-claudecode.git` @ `454bae017356`  
Skills: 12 · Agentes: 19

Versão: `2026.1009.0`

**Padrões de risco:** nenhum

**Domínios citados:** github.com (2), nodejs.org (1)

## supabase

Upstream: `https://github.com/supabase/agent-skills.git` @ `c9be0e931b79`  
Skills: 2 · Agentes: 0

Versão: `2026.1009.0`

**Padrões de risco:** nenhum

**Domínios citados:** supabase.com (28), www.postgresql.org (19), github.com (3), mcp.supabase.com (2), wiki.postgresql.org (1)

## vercel

Upstream: `https://github.com/vercel-labs/agent-skills.git` @ `063bee94c3f4`  
Skills: 9 · Agentes: 0

Versão: `2026.1009.0`

**Padrões de risco:** 
- ⚠️ `spawn de processo` em `skills/vercel-optimize/lib/sanitizers/undeclared-dep.mjs:10`
- ⚠️ `spawn de processo` em `skills/vercel-optimize/lib/vercel.mjs:3`
- ⚠️ `spawn de processo` em `skills/vercel-optimize/lib/verify-claim.mjs:4`

**Domínios citados:** vercel.com (170), nextjs.org (117), react.dev (60), github.com (32), kit.svelte.dev (23), web.dev (15), docs.swmansion.com (12), docs.expo.dev (10), example.com (10), docs.astro.build (8), nuxt.com (8), workflow-sdk.dev (8), zeego.dev (8), swr.vercel.app (7), legendapp.com (5), svelte.dev (5), oss.callstack.com (4), turborepo.dev (4), developer.mozilla.org (3), esbuild.github.io (3), reactnative.dev (3), skills.sh (3), vite.dev (3), webpack.js.org (3), www.npmjs.com (3), analytics.example.com (2), api.example.com (2), csstriggers.com (2), developers.notion.com (2), docs.anthropic.com (2), docs.stripe.com (2), gist.github.com (2), jsfiddle.net (2), platform.openai.com (2), raw.githubusercontent.com (2), reactnavigation.org (2), claude-skills-deploy.vercel.com (1), claude.ai (1), codex-deploy-skills.vercel.sh (1), my-app-abc123.vercel.app (1), x.com (1), your-domain.tld (1)

**⚙️ Código executável (92 arquivos)** — revise o diff destes com atenção:
- `skills/deploy-to-vercel`: 2 arquivo(s)
- `skills/vercel-optimize`: 90 arquivo(s)

**🌐 Endpoints chamados pelo código:**
- `https://codex-deploy-skills.vercel.sh/api/deploy` em `skills/deploy-to-vercel/resources/deploy-codex.sh`
- `https://claude-skills-deploy.vercel.com/api/deploy` em `skills/deploy-to-vercel/resources/deploy.sh`
- `https://web.dev/articles/vitals` em `skills/vercel-optimize/lib/gates/cwv-poor.mjs`
- `https://vercel.com/docs/incremental-static-regeneration` em `skills/vercel-optimize/lib/gates/isr-overrevalidation.mjs`
- `https://nextjs.org/docs/app/building-your-application/routing/middleware` em `skills/vercel-optimize/lib/gates/middleware-heavy.mjs`
- `https://developers.notion.com/reference/request-limits` em `skills/vercel-optimize/lib/sanitizers/rate-limit.mjs`
- `https://docs.anthropic.com/en/api/rate-limits` em `skills/vercel-optimize/lib/sanitizers/rate-limit.mjs`
- `https://docs.stripe.com/rate-limits` em `skills/vercel-optimize/lib/sanitizers/rate-limit.mjs`
- `https://platform.openai.com/docs/guides/rate-limits` em `skills/vercel-optimize/lib/sanitizers/rate-limit.mjs`
- `https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents` em `skills/vercel-optimize/lib/scanners/cache-components-suspense-dedupe.mjs`
- `https://nextjs.org/docs/app/api-reference/directives/use-cache` em `skills/vercel-optimize/lib/scanners/cache-components-suspense-dedupe.mjs`
- `https://nextjs.org/docs/app/guides/migrating-to-cache-components` em `skills/vercel-optimize/lib/scanners/cache-components-suspense-dedupe.mjs`
- `https://vercel.com/docs/fluid-compute` em `skills/vercel-optimize/lib/scanners/edge-heavy-import.mjs`
- `https://vercel.com/docs/functions/runtimes/edge-runtime` em `skills/vercel-optimize/lib/scanners/edge-heavy-import.mjs`
- `https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config` em `skills/vercel-optimize/lib/scanners/force-dynamic.mjs`
- `https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config` em `skills/vercel-optimize/lib/scanners/headers-in-page.mjs`
- `https://nextjs.org/docs/app/building-your-application/caching` em `skills/vercel-optimize/lib/scanners/headers-in-page.mjs`
- `https://vercel.com/docs/image-optimization` em `skills/vercel-optimize/lib/scanners/large-static-asset.mjs`
- `https://vercel.com/docs/manage-cdn-usage` em `skills/vercel-optimize/lib/scanners/large-static-asset.mjs`
- `https://vercel.com/docs/caching/cache-control-headers` em `skills/vercel-optimize/lib/scanners/max-age-without-s-maxage.mjs`
- `https://vercel.com/docs/caching/cdn-cache` em `skills/vercel-optimize/lib/scanners/max-age-without-s-maxage.mjs`
- `https://nextjs.org/docs/app/building-your-application/routing/middleware` em `skills/vercel-optimize/lib/scanners/middleware-broad-matcher.mjs`
- `https://nextjs.org/docs/app/building-your-application/caching` em `skills/vercel-optimize/lib/scanners/missing-cache-headers.mjs`
- `https://vercel.com/docs/caching/cache-control-headers` em `skills/vercel-optimize/lib/scanners/missing-cache-headers.mjs`
- `https://vercel.com/docs/caching/cdn-cache` em `skills/vercel-optimize/lib/scanners/missing-cache-headers.mjs`
- `https://vercel.com/docs/functions/configuring-functions/region` em `skills/vercel-optimize/lib/scanners/region-pin-in-config.mjs`
- `https://nextjs.org/docs/messages/improper-devtool` em `skills/vercel-optimize/lib/scanners/source-maps-production.mjs`
- `https://kit.svelte.dev/docs/adapter-vercel` em `skills/vercel-optimize/lib/scanners/sveltekit-prerender-missing.mjs`
- `https://kit.svelte.dev/docs/page-options` em `skills/vercel-optimize/lib/scanners/sveltekit-prerender-missing.mjs`
- `https://vercel.com/docs/incremental-static-regeneration` em `skills/vercel-optimize/lib/scanners/sveltekit-prerender-missing.mjs`
- `https://turborepo.dev/docs/crafting-your-repository/caching` em `skills/vercel-optimize/lib/scanners/turbo-force-bypass.mjs`
- `https://vercel.com/docs/builds` em `skills/vercel-optimize/lib/scanners/turbo-force-bypass.mjs`
- `https://vercel.com/docs/monorepos` em `skills/vercel-optimize/lib/scanners/turbo-force-bypass.mjs`
- `https://nextjs.org/docs/app/api-reference/components/image` em `skills/vercel-optimize/lib/scanners/unoptimized-image.mjs`
- `https://vercel.com/docs/image-optimization` em `skills/vercel-optimize/lib/scanners/unoptimized-image.mjs`
- `https://nextjs.org/docs/app/api-reference/directives/use-cache` em `skills/vercel-optimize/lib/scanners/use-cache-date-stamp.mjs`
- `https://nextjs.org/docs/app/api-reference/functions/cacheLife` em `skills/vercel-optimize/lib/scanners/use-cache-date-stamp.mjs`
- `https://nextjs.org/docs/app/api-reference/functions/cache` em `skills/vercel-optimize/scripts/check-citations.mjs`
- `https://nextjs.org/docs/app/api-reference/functions/cache-life` em `skills/vercel-optimize/scripts/check-citations.mjs`
- `https://nextjs.org/docs/app/api-reference/functions/cache-tag` em `skills/vercel-optimize/scripts/check-citations.mjs`
- `https://nextjs.org/docs/app/api-reference/functions/revalidate-path` em `skills/vercel-optimize/scripts/check-citations.mjs`
- `https://nextjs.org/docs/app/api-reference/functions/revalidate-tag` em `skills/vercel-optimize/scripts/check-citations.mjs`

**Arquivos não-texto ignorados:** `deploy-to-vercel/Archive.zip`

