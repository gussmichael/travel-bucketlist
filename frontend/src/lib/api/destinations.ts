import { api } from './client';
import type { Destination } from '../types';

interface DestinationParams {
  q?: string;
  category?: string;
  country?: string;
  limit?: number;
  offset?: number;
}

export async function fetchDestinations(params: DestinationParams = {}): Promise<Destination[]> {
  const searchParams = new URLSearchParams();
  if (params.q) searchParams.set('q', params.q);
  if (params.category) searchParams.set('category', params.category);
  if (params.country) searchParams.set('country', params.country);
  if (params.limit) searchParams.set('limit', String(params.limit));
  if (params.offset) searchParams.set('offset', String(params.offset));
  const qs = searchParams.toString();
  return api.get<Destination[]>(`/destinations${qs ? `?${qs}` : ''}`);
}

export async function fetchCountries(category?: string): Promise<string[]> {
  const qs = category ? `?category=${category}` : '';
  return api.get<string[]>(`/destinations/countries${qs}`);
}
