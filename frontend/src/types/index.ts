export interface ReportPublicItem {
  id: string;
  case_number: string;
  first_name: string;
  last_name: string;
  age_at_disappearance: number;
  gender: string;
  disappearance_date: string;
  department: string;
  municipality: string;
  physical_description: string;
  primary_photo_url?: string;
  is_minor: boolean;
  status: string;
  published_at?: string;
  resolution_notes?: string;
}

export interface CaseMilestone {
  date: string;
  title: string;
  description: string;
  status: "completed" | "current" | "pending";
}

export interface ReportDetail extends ReportPublicItem {
  nickname?: string;
  neighborhood_zone?: string;
  approximate_latitude: number;
  approximate_longitude: number;
  clothing_description: string;
  circumstances: string;
  medical_conditions?: string;
  vulnerability_flag: boolean;
  photos: {
    id: string;
    storage_key: string;
    url: string;
    is_primary: boolean;
    original_filename: string;
  }[];
  timeline?: CaseMilestone[];
}

export interface MapPoint {
  id: string;
  case_number: string;
  full_name: string;
  age_at_disappearance: number;
  gender: string;
  department: string;
  municipality: string;
  disappearance_date: string;
  approximate_latitude: number;
  approximate_longitude: number;
  photo_url?: string;
  is_minor: boolean;
  status: string;
}

export interface UserSession {
  user_id: string;
  email: string;
  full_name: string;
  role: "admin" | "moderator" | "reporter" | "citizen";
  access_token: string;
}

export interface DepartmentItem {
  id: string;
  name: string;
  code: string;
  type: "department" | "autonomous_region";
  latitude: number;
  longitude: number;
  is_active: boolean;
  created_at: string;
  municipalities_count?: number;
}

export interface MunicipalityItem {
  id: string;
  department_id: string;
  department_name?: string;
  name: string;
  code: string;
  latitude: number;
  longitude: number;
  is_active: boolean;
  created_at: string;
}

export interface GeographicSummary {
  total_departments: number;
  total_municipalities: number;
  active_departments: number;
  active_municipalities: number;
  source: string;
  last_update: string;
}
