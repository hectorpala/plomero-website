import { readFileSync, writeFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CACHE_FILE = join(__dirname, 'cache-places.json');
const CACHE_TTL_DAYS = 30;

function loadCache() {
  if (!existsSync(CACHE_FILE)) return {};
  try {
    return JSON.parse(readFileSync(CACHE_FILE, 'utf-8'));
  } catch {
    return {};
  }
}

function saveCache(cache) {
  writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2), 'utf-8');
}

function isCacheValid(entry) {
  if (!entry || !entry.timestamp) return false;
  const age = Date.now() - entry.timestamp;
  return age < CACHE_TTL_DAYS * 24 * 60 * 60 * 1000;
}

async function geocodeColonia(colonia, apiKey) {
  const query = encodeURIComponent(`${colonia}, Culiacán, Sinaloa, México`);
  const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${query}&key=${apiKey}`;
  const res = await fetch(url);
  const data = await res.json();

  if (data.status !== 'OK' || !data.results.length) {
    return null;
  }

  const result = data.results[0];
  return {
    lat: result.geometry.location.lat,
    lng: result.geometry.location.lng,
    formatted_address: result.formatted_address,
    postal_code: result.address_components?.find(c => c.types.includes('postal_code'))?.long_name || null
  };
}

async function nearbyPlaces(lat, lng, apiKey, radius = 500) {
  // Uses Places API (New) - Nearby Search
  const url = 'https://places.googleapis.com/v1/places:searchNearby';

  const body = {
    includedTypes: ['school', 'hospital', 'park', 'church', 'shopping_mall', 'supermarket', 'bank', 'pharmacy', 'restaurant', 'gas_station'],
    maxResultCount: 15,
    locationRestriction: {
      circle: {
        center: { latitude: lat, longitude: lng },
        radius: radius
      }
    },
    languageCode: 'es'
  };

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Goog-Api-Key': apiKey,
      'X-Goog-FieldMask': 'places.displayName,places.types,places.formattedAddress,places.location,places.rating,places.userRatingCount'
    },
    body: JSON.stringify(body)
  });

  const data = await res.json();

  if (!data.places || !data.places.length) {
    return [];
  }

  return data.places.map(place => ({
    name: place.displayName?.text || 'Sin nombre',
    type: place.types?.[0] || 'unknown',
    address: place.formattedAddress || '',
    rating: place.rating || null,
    total_ratings: place.userRatingCount || 0,
    distance_meters: haversine(lat, lng, place.location?.latitude, place.location?.longitude)
  }));
}

function haversine(lat1, lng1, lat2, lng2) {
  const R = 6371000;
  const toRad = d => d * Math.PI / 180;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  return Math.round(2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)));
}

export async function getLocalPlaces(colonia, apiKey, radiusMeters = 500) {
  const cache = loadCache();
  const cacheKey = `${colonia}_${radiusMeters}`;

  if (cache[cacheKey] && isCacheValid(cache[cacheKey])) {
    return { ...cache[cacheKey].data, source: 'cache' };
  }

  const geo = await geocodeColonia(colonia, apiKey);
  if (!geo) {
    return { error: `No se pudo geocodificar la colonia "${colonia}"` };
  }

  const places = await nearbyPlaces(geo.lat, geo.lng, apiKey, radiusMeters);

  const result = {
    colonia,
    coordinates: { lat: geo.lat, lng: geo.lng },
    formatted_address: geo.formatted_address,
    postal_code: geo.postal_code,
    radius_meters: radiusMeters,
    nearby_places: places,
    landmarks: places.filter(p =>
      ['school', 'hospital', 'park', 'church', 'shopping_mall', 'supermarket', 'bank', 'pharmacy'].includes(p.type)
    ),
    summary: generateSummary(colonia, places)
  };

  cache[cacheKey] = { data: result, timestamp: Date.now() };
  saveCache(cache);

  return { ...result, source: 'google_api' };
}

function generateSummary(colonia, places) {
  if (!places.length) return `No se encontraron lugares cercanos a ${colonia}.`;

  const landmarks = places
    .filter(p => ['school', 'hospital', 'park', 'church', 'shopping_mall', 'supermarket'].includes(p.type))
    .slice(0, 3);

  if (!landmarks.length) {
    return `Zona ${colonia} con ${places.length} establecimientos cercanos.`;
  }

  const refs = landmarks.map(l => {
    const dist = l.distance_meters < 200 ? 'junto a' : `a ${Math.round(l.distance_meters / 100) * 100}m de`;
    return `${dist} ${l.name}`;
  });

  return `Servicio de plomería en ${colonia}, ${refs.join(', ')}.`;
}
