export interface Destination {
  id: number;
  name: string;
  category: 'city' | 'landmark';
  country: string;
  country_code: string | null;
  region: string | null;
  latitude: number;
  longitude: number;
  population: number | null;
  description: string | null;
  image_url: string | null;
  in_bucketlist: boolean;
  bucket_item_id: number | null;
}

export interface BucketListItem {
  id: number;
  destination_id: number;
  visited: boolean;
  visited_date: string | null;
  notes: string | null;
  created_at: string;
  destination_name: string;
  destination_category: 'city' | 'landmark';
  destination_country: string;
  destination_latitude: number;
  destination_longitude: number;
  destination_image_url: string | null;
}

export interface MapMarker {
  bucket_item_id: number;
  destination_id: number;
  name: string;
  category: 'city' | 'landmark';
  country: string;
  latitude: number;
  longitude: number;
  visited: boolean;
}
