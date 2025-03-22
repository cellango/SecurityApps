export type ApplicationType = 'internal' | 'vendor';
export type ApplicationState = 'planning' | 'development' | 'testing' | 'production' | 'deprecated' | 'retired';

export interface Application {
  id: number;
  name: string;
  description: string;
  application_type: ApplicationType;
  state: ApplicationState;
  owner_id: string;
  owner_email: string;
  department_name: string;
  team_name: string;
  test_score: number;
  data_classification: string;
  authentication_method: string;
  requires_2fa: boolean;
  vendor_name?: string;
  vendor_contact?: string;
  contract_expiration?: string;
  created_at?: string;
  updated_at?: string;
}

export interface SearchResult {
  id: number;
  name: string;
  description: string;
  application_type: ApplicationType;
  state: ApplicationState;
}

export interface Control {
  id: number;
  name: string;
  description: string;
  type: string;
  priority: 'low' | 'medium' | 'high';
  status: 'implemented' | 'not_implemented' | 'in_progress';
  implementation_details?: string;
  last_tested_date?: string;
  next_review_date?: string;
}

export interface SecurityControlsProps {
  applicationId: number;
}
