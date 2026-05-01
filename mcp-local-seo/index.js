#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { readFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { getLocalPlaces } from './places.js';
import { searchKeywords, findOpportunities } from './search-console.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load .env
const envPath = join(__dirname, '.env');
if (existsSync(envPath)) {
  const envContent = readFileSync(envPath, 'utf-8');
  for (const line of envContent.split('\n')) {
    const [key, ...vals] = line.split('=');
    if (key && vals.length) {
      process.env[key.trim()] = vals.join('=').trim();
    }
  }
}

const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY;

const server = new Server(
  { name: 'local-seo', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

// List tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'get_local_places',
      description: 'Obtiene landmarks y negocios reales cerca de una colonia en Culiacán usando Google Places API. Útil para generar contenido único por zona con referencias locales reales.',
      inputSchema: {
        type: 'object',
        properties: {
          colonia: {
            type: 'string',
            description: 'Nombre de la colonia (ej: "Las Quintas", "Tres Ríos", "Centro")'
          },
          radius_meters: {
            type: 'number',
            description: 'Radio de búsqueda en metros (default: 500)',
            default: 500
          }
        },
        required: ['colonia']
      }
    },
    {
      name: 'search_keywords',
      description: 'Consulta Google Search Console para ver keywords reales: clics, impresiones, CTR y posición promedio del sitio plomeroculiacanpro.mx. Puede filtrar por keyword o por URL de página.',
      inputSchema: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'Filtrar keywords que contengan este texto (ej: "drenaje", "boiler", "culiacan")'
          },
          page_filter: {
            type: 'string',
            description: 'Filtrar por URL de página (ej: "/servicios/destape-de-drenajes/")'
          },
          days: {
            type: 'number',
            description: 'Días hacia atrás a consultar (default: 28)',
            default: 28
          },
          limit: {
            type: 'number',
            description: 'Máximo de keywords a retornar (default: 50)',
            default: 50
          }
        }
      }
    },
    {
      name: 'find_opportunities',
      description: 'Analiza Search Console para encontrar oportunidades SEO: keywords cerca de página 1 (quick wins) y keywords con muchas impresiones pero 0 clics (snippets débiles).',
      inputSchema: {
        type: 'object',
        properties: {
          min_position: {
            type: 'number',
            description: 'Posición mínima para quick wins (default: 5)',
            default: 5
          },
          max_position: {
            type: 'number',
            description: 'Posición máxima para quick wins (default: 20)',
            default: 20
          },
          min_impressions: {
            type: 'number',
            description: 'Mínimo de impresiones (default: 10)',
            default: 10
          },
          days: {
            type: 'number',
            description: 'Días hacia atrás (default: 28)',
            default: 28
          }
        }
      }
    }
  ]
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result;

    switch (name) {
      case 'get_local_places':
        if (!GOOGLE_MAPS_API_KEY) {
          result = { error: 'GOOGLE_MAPS_API_KEY no configurada en mcp-local-seo/.env' };
        } else {
          result = await getLocalPlaces(args.colonia, GOOGLE_MAPS_API_KEY, args.radius_meters || 500);
        }
        break;

      case 'search_keywords':
        result = await searchKeywords({
          query: args.query,
          pageFilter: args.page_filter,
          days: args.days || 28,
          limit: args.limit || 50
        });
        break;

      case 'find_opportunities':
        result = await findOpportunities({
          minPosition: args.min_position || 5,
          maxPosition: args.max_position || 20,
          minImpressions: args.min_impressions || 10,
          days: args.days || 28
        });
        break;

      default:
        result = { error: `Herramienta "${name}" no encontrada` };
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(result, null, 2)
      }]
    };
  } catch (err) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ error: err.message }, null, 2)
      }]
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
