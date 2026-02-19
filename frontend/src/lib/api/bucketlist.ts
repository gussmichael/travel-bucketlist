import { api } from './client';
import type { BucketListItem, MapMarker } from '../types';

interface BucketListParams {
  visited?: boolean;
  category?: string;
}

export async function fetchBucketList(params: BucketListParams = {}): Promise<BucketListItem[]> {
  const searchParams = new URLSearchParams();
  if (params.visited !== undefined) searchParams.set('visited', String(params.visited));
  if (params.category) searchParams.set('category', params.category);
  const qs = searchParams.toString();
  return api.get<BucketListItem[]>(`/bucketlist${qs ? `?${qs}` : ''}`);
}

export async function addToBucketList(destinationId: number, notes?: string): Promise<BucketListItem> {
  return api.post<BucketListItem>('/bucketlist', { destination_id: destinationId, notes });
}

export async function updateBucketListItem(
  itemId: number,
  data: { visited?: boolean; visited_date?: string; notes?: string }
): Promise<BucketListItem> {
  return api.patch<BucketListItem>(`/bucketlist/${itemId}`, data);
}

export async function removeFromBucketList(itemId: number): Promise<void> {
  return api.delete(`/bucketlist/${itemId}`);
}

export async function fetchMapMarkers(visitedOnly = false): Promise<MapMarker[]> {
  const qs = visitedOnly ? '?visited_only=true' : '';
  return api.get<MapMarker[]>(`/bucketlist/map${qs}`);
}
